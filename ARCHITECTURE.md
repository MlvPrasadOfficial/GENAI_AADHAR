# Aadhaar KYC Face Matching Pipeline - Architecture

## System Overview

```mermaid
flowchart TB
    subgraph INPUT["INPUT LAYER"]
        CLI["main.py<br/>CLI Entry Point"]
        SINGLE["Single Mode<br/>--aadhaar + --selfie"]
        BATCH["Batch Mode<br/>--batch pairs.csv"]
        CSV["pairs.csv<br/>90 pairs (9x10)"]
    end

    subgraph CONFIG["CONFIGURATION"]
        YAML["config.yaml<br/>All tunable parameters"]
        LOADER["config_loader.py<br/>YAML parser + validator"]
    end

    subgraph PIPELINE["PIPELINE ORCHESTRATOR"]
        ORCH["orchestrator.py<br/>KYCPipelineOrchestrator"]
    end

    subgraph OUTPUT["OUTPUT LAYER"]
        LOGGER["result_logger.py<br/>Per-run log folders"]
        LOGDIR["logs/<br/>README.md + result.txt + crops"]
        EXIT["Exit Code<br/>0=MATCH 1=NO_MATCH 2=ERROR"]
    end

    CLI --> SINGLE & BATCH
    BATCH --> CSV
    YAML --> LOADER --> ORCH
    SINGLE & BATCH --> ORCH
    ORCH --> LOGGER --> LOGDIR
    ORCH --> EXIT
```

## Complete Pipeline Flow

```mermaid
flowchart TD
    START(["Start: run(aadhaar_bytes, selfie_bytes)"])

    subgraph STAGE1["STAGE 1: Image Loading"]
        S1A["bytes_to_bgr(aadhaar_bytes)<br/>EXIF correction + PDF extraction"]
        S1B["bytes_to_bgr(selfie_bytes)<br/>EXIF correction"]
        PDF{"PDF detected?<br/>%PDF- magic bytes"}
        PDFEX["PyMuPDF: extract<br/>embedded image or<br/>render page at 2x"]
        JPG["OpenCV: imdecode<br/>BGR numpy array"]
    end

    subgraph STAGE2["STAGE 2: Quality Assessment & Enhancement"]
        QA["quality_score(image)<br/>Laplacian variance"]
        QCHECK{"quality < 0.4?"}
        ESRGAN["Real-ESRGAN<br/>2x upscale<br/>(tile=512, GPU)"]
        SKIP["Skip enhancement<br/>(already sharp)"]
        S2OUT["enhanced_img + quality_score"]
    end

    subgraph STAGE2B["STAGE 2b: Preprocessing (Optional)"]
        CLAHE{"CLAHE enabled?<br/>(Aadhaar only)"}
        CAPP["apply_clahe()<br/>LAB L-channel<br/>clip=2.0, tile=8"]
        GRAY{"Grayscale<br/>normalize?"}
        GAPP["to_grayscale_bgr()<br/>Remove color domain gap"]
    end

    subgraph STAGE3["STAGE 3: Face Detection + Embedding"]
        CACHE{"Embedding<br/>cache hit?<br/>SHA-256 lookup"}
        CHIT["Cache HIT<br/>Return stored FaceResult"]
        
        DET["RetinaFace detect<br/>det_size=640x640<br/>det_thresh=0.7"]
        NOFACE{"Faces<br/>found?"}
        FALLBACK["Retry detection<br/>det_thresh=0.5"]
        NOFACE2{"Faces<br/>found?"}
        ERROR1["NoFaceDetectedError"]
        
        BEST["Select best face<br/>argmax(det_score)"]
        ALIGN["5-point landmark<br/>alignment -> 112x112 crop"]
        EMBED["ArcFace R50<br/>512-d embedding<br/>L2-normalized"]
        
        TTA{"TTA mode?"}
        FLIP["Flip augment<br/>avg(orig, flipped)"]
        ENSEMBLE["Ensemble augment<br/>avg(orig, flip,<br/>bright, dark, blur)"]
        NOTTA["Single embedding"]
        
        DEMO["Gender + Age<br/>estimation"]
        LMK["68-point 3D landmarks<br/>+ pose (pitch/yaw/roll)"]
        
        CSTORE["Cache MISS<br/>Store FaceResult"]
    end

    subgraph STAGE3B["STAGE 3b: Crop Restoration (Optional)"]
        CROP{"Crop restore<br/>enabled?"}
        BILATERAL["Bilateral filter<br/>d=5, sigma=50"]
        GFPGAN["GFPGAN restore<br/>(if model available)"]
    end

    subgraph STAGE4["STAGE 4: Similarity Scoring"]
        COS["Cosine similarity<br/>dot(emb_a, emb_s)"]
        
        DUAL{"Dual-path<br/>enabled?"}
        ORIG["Process original<br/>(unenhanced) Aadhaar"]
        COMPARE{"Original score<br/>> enhanced?"}
        USEORIGINAL["Use original path"]
        USEENHANCED["Use enhanced path"]
    end

    subgraph STAGE4C["STAGE 4c: AdaFace Fusion (Optional)"]
        ADA{"AdaFace<br/>available?"}
        ADAEMB["AdaFace IR-101<br/>512-d embeddings"]
        ADAFUSE["Fused score<br/>0.7*ArcFace + 0.3*AdaFace"]
    end

    subgraph STAGE4D["STAGE 4d: S-Norm Calibration (Optional)"]
        SNORM{"S-norm<br/>available?"}
        ZNORM["Z-score normalize<br/>against impostor cohort"]
    end

    subgraph STAGE4E["STAGE 4e: Multi-Metric Computation"]
        L2["L2 distance<br/>l2_score = e^(-1.5*dist)"]
        SSIM["SSIM<br/>Structural similarity<br/>on 112x112 crops"]
        LMKSCORE["Landmark geometry<br/>12 age-invariant ratios<br/>e^(-20*avg_diff)"]
        POSE["Pose difference<br/>pitch/yaw/roll delta"]
        FUSED["Fused score<br/>55% cos + 25% lmk<br/>+ 10% L2 + 10% SSIM"]
    end

    subgraph STAGE5["STAGE 5: Decision & VLM Gate"]
        DECIDE{"Cosine score<br/>threshold check"}
        MATCH_ZONE["MATCH ZONE<br/>score >= 0.60"]
        UNCERTAIN_ZONE["UNCERTAIN ZONE<br/>0.40 <= score < 0.60"]
        NOMATCH_ZONE["NO MATCH ZONE<br/>score < 0.40"]

        QLOW1{"Quality low?"}
        VLM_YES["Invoke VLM guard"]
        VLM_NO["Skip VLM"]

        AGEGAP{"Age gap > 5yr?"}
        RELAX["Relax thresholds<br/>-0.01/yr (max -0.10)"]

        subgraph VLM["VLM Guard (Ollama)"]
            VLMCALL["HTTP POST to Ollama<br/>Qwen2.5-VL-7B"]
            VLMPROMPT["Prompt: Compare bone<br/>structure, ignore aging<br/>+ age-conditioned guidance"]
            VLMPARSE["Parse JSON response<br/>(fallback: regex)"]
            VLMOUT["VLMVerdict<br/>same_person + confidence<br/>+ reasoning"]
        end
    end

    subgraph STAGE6["STAGE 6: Final Decision Fusion"]
        FUSE["_fuse_decision()"]

        subgraph HIGHSCORE["Score >= Match Threshold"]
            HS_VLM{"VLM says<br/>same person?"}
            HS_YES["MATCH<br/>conf += 8 (VLM bonus)"]
            HS_NO["NO MATCH<br/>conf -= 20 (VLM override)"]
            HS_NONE["MATCH<br/>(no VLM available)"]
        end

        subgraph MIDSCORE["Uncertain Zone"]
            MS_VLM{"VLM says<br/>same person?"}
            MS_YES["MATCH<br/>conf += 8 (VLM confirms)"]
            MS_NO["NO MATCH<br/>conf -= 10 (VLM rejects)"]
            MS_NONE["NO MATCH<br/>(no VLM to confirm)"]
        end

        LOWSCORE["NO MATCH<br/>score too low"]

        AGEADJUST{"Age gap > 5yr<br/>AND VLM confirms?"}
        AGEBONUS["conf += 5<br/>age gap VLM bonus"]
        QPENALTY{"Quality low?"}
        QPEN["conf -= 5"]
        GCHECK{"Gender<br/>mismatch?"}
        GPEN["conf -= penalty"]
        CLAMP["Clamp confidence<br/>to 0.0 - 99.0"]
    end

    subgraph STAGE6B["STAGE 6b: Confidence Calibration (Optional)"]
        CAL{"Calibration<br/>enabled?"}
        PLATT["Platt scaling<br/>P = 1/(1+exp(-(15s-7.5)))<br/>score -> probability %"]
    end

    subgraph STAGE7["STAGE 7: Logging"]
        LOG["result_logger.py"]
        LOGFILES["Log folder:<br/>result.txt + README.md<br/>+ face crops + metrics"]
        BATCHLOG["Batch: summary.txt<br/>+ README.md table"]
    end

    RESULT(["PipelineResult<br/>match + confidence + metrics"])

    %% Flow connections
    START --> S1A & S1B
    S1A --> PDF
    PDF -->|Yes| PDFEX --> QA
    PDF -->|No| JPG --> QA
    S1B --> JPG

    QA --> QCHECK
    QCHECK -->|Yes| ESRGAN --> S2OUT
    QCHECK -->|No| SKIP --> S2OUT

    S2OUT --> CLAHE
    CLAHE -->|Yes| CAPP --> GRAY
    CLAHE -->|No| GRAY
    GRAY -->|Yes| GAPP --> CACHE
    GRAY -->|No| CACHE

    CACHE -->|Hit| CHIT --> COS
    CACHE -->|Miss| DET
    DET --> NOFACE
    NOFACE -->|Yes| BEST
    NOFACE -->|No| FALLBACK --> NOFACE2
    NOFACE2 -->|Yes| BEST
    NOFACE2 -->|No| ERROR1

    BEST --> ALIGN --> EMBED --> TTA
    TTA -->|Flip| FLIP --> DEMO
    TTA -->|Ensemble| ENSEMBLE --> DEMO
    TTA -->|None| NOTTA --> DEMO
    DEMO --> LMK --> CSTORE --> CROP

    CROP -->|Yes| BILATERAL --> COS
    CROP -->|No| COS

    COS --> DUAL
    DUAL -->|Yes| ORIG --> COMPARE
    COMPARE -->|Yes| USEORIGINAL --> ADA
    COMPARE -->|No| USEENHANCED --> ADA
    DUAL -->|No| ADA

    ADA -->|Yes| ADAEMB --> ADAFUSE --> SNORM
    ADA -->|No| SNORM

    SNORM -->|Yes| ZNORM --> L2
    SNORM -->|No| L2

    L2 --> SSIM --> LMKSCORE --> POSE --> FUSED

    FUSED --> DECIDE
    DECIDE -->|">= 0.60"| MATCH_ZONE --> QLOW1
    DECIDE -->|"0.40 - 0.60"| UNCERTAIN_ZONE --> VLM_YES
    DECIDE -->|"< 0.40"| NOMATCH_ZONE --> LOWSCORE

    QLOW1 -->|Yes| VLM_YES
    QLOW1 -->|No| VLM_NO

    MATCH_ZONE --> AGEGAP
    UNCERTAIN_ZONE --> AGEGAP
    AGEGAP -->|Yes| RELAX
    AGEGAP -->|No| FUSE

    VLM_YES --> VLMCALL --> VLMPROMPT --> VLMPARSE --> VLMOUT --> FUSE
    VLM_NO --> FUSE
    RELAX --> FUSE

    FUSE --> HIGHSCORE & MIDSCORE & LOWSCORE
    HS_VLM -->|Yes| HS_YES
    HS_VLM -->|No| HS_NO
    HS_VLM -->|None| HS_NONE
    MS_VLM -->|Yes| MS_YES
    MS_VLM -->|No| MS_NO
    MS_VLM -->|None| MS_NONE

    HS_YES & HS_NO & HS_NONE & MS_YES & MS_NO & MS_NONE & LOWSCORE --> AGEADJUST
    AGEADJUST -->|Yes| AGEBONUS --> QPENALTY
    AGEADJUST -->|No| QPENALTY
    QPENALTY -->|Yes| QPEN --> GCHECK
    QPENALTY -->|No| GCHECK
    GCHECK -->|Yes| GPEN --> CLAMP
    GCHECK -->|No| CLAMP

    CLAMP --> CAL
    CAL -->|Yes| PLATT --> LOG
    CAL -->|No| LOG

    LOG --> LOGFILES & BATCHLOG
    LOGFILES --> RESULT
    BATCHLOG --> RESULT
```

## Module Dependency Map

```mermaid
flowchart LR
    subgraph CLI["CLI Layer"]
        MAIN["main.py"]
    end

    subgraph CORE["Core Pipeline"]
        ORCH["orchestrator.py"]
        ENH["enhancement.py"]
        FP["face_processor.py"]
        SIM["similarity.py"]
        VLM["vlm_guard.py"]
    end

    subgraph OPTIONAL["Optional Modules"]
        ADA["adaface.py"]
        SNORM["score_norm.py"]
        CAL["confidence_calibrator.py"]
        CROP["crop_restore.py"]
    end

    subgraph UTILS["Utilities"]
        IMG["image_utils.py"]
        CFG["config_loader.py"]
        LOG["result_logger.py"]
        CACHE["embedding_cache.py"]
        EXC["exceptions.py"]
    end

    subgraph EXTERNAL["External Services"]
        OLLAMA["Ollama Server<br/>Qwen2.5-VL-7B"]
        IF["InsightFace<br/>buffalo_l"]
        ESRGAN["Real-ESRGAN<br/>RRDBNet"]
    end

    MAIN --> ORCH & CFG & LOG
    ORCH --> ENH & FP & SIM & VLM
    ORCH --> ADA & SNORM & CAL & CROP & CACHE
    ORCH --> IMG & EXC
    ENH --> ESRGAN
    FP --> IF
    VLM --> OLLAMA
    VLM --> IMG
    SIM --> EXC
    LOG --> IMG
```

## Decision Tree: Match / No Match

```mermaid
flowchart TD
    SCORE["Cosine Score"]
    
    HIGH{"score >= 0.60<br/>(match threshold)"}
    MID{"score >= 0.40<br/>(uncertain low)"}
    LOW["NO MATCH<br/>Score too low"]

    HQUAL{"Image quality<br/>low?"}
    HVLM{"VLM verdict?"}
    HMATCH["MATCH<br/>confidence = score*100 + 8"]
    HNOMATCH["NO MATCH<br/>confidence = score*100 - 20"]
    HSKIP["MATCH<br/>confidence = score*100"]

    MVLM{"VLM verdict?"}
    MMATCH["MATCH<br/>confidence = score*100 + 8"]
    MNOMATCH["NO MATCH<br/>confidence = score*100 - 10"]
    MNOVLM["NO MATCH<br/>No VLM to confirm"]

    SCORE --> HIGH
    HIGH -->|Yes| HQUAL
    HIGH -->|No| MID

    HQUAL -->|"Yes (invoke VLM)"| HVLM
    HQUAL -->|"No (skip VLM)"| HSKIP

    HVLM -->|"True"| HMATCH
    HVLM -->|"False"| HNOMATCH
    HVLM -->|"None"| HSKIP

    MID -->|Yes| MVLM
    MID -->|No| LOW

    MVLM -->|"True"| MMATCH
    MVLM -->|"False"| MNOMATCH
    MVLM -->|"None"| MNOVLM

    style HMATCH fill:#2d6a2d,color:#fff
    style HSKIP fill:#2d6a2d,color:#fff
    style MMATCH fill:#2d6a2d,color:#fff
    style HNOMATCH fill:#8b1a1a,color:#fff
    style MNOMATCH fill:#8b1a1a,color:#fff
    style MNOVLM fill:#8b1a1a,color:#fff
    style LOW fill:#8b1a1a,color:#fff
```

## Multi-Metric Fusion Weights

```mermaid
pie title Score Fusion Weights (Default)
    "Cosine Similarity" : 55
    "Landmark Geometry" : 25
    "L2 Distance" : 10
    "SSIM" : 10
```

## Quality-Adaptive Weight Shift

```mermaid
pie title Score Fusion Weights (Low Quality)
    "Cosine Similarity" : 50
    "Landmark Geometry" : 35
    "L2 Distance" : 10
    "SSIM" : 5
```

## Embedding Pipeline Detail

```mermaid
flowchart LR
    IMG["Input Image<br/>BGR uint8"] 
    --> DET["RetinaFace<br/>Detection"]
    --> ALIGN["5-point Landmark<br/>Alignment"]
    --> CROP["112x112<br/>Normalized Crop"]
    --> ARC["ArcFace R50<br/>Forward Pass"]
    --> EMB["512-d Vector<br/>L2 Normalized"]

    CROP --> FLIP["Horizontal Flip"]
    FLIP --> ARC2["ArcFace R50<br/>Forward Pass"]
    ARC2 --> FLIP_EMB["512-d Vector"]

    EMB & FLIP_EMB --> AVG["Average +<br/>Re-normalize"]
    AVG --> FINAL["Final 512-d<br/>Embedding"]

    style FINAL fill:#1a5276,color:#fff
```

## Batch Processing Flow

```mermaid
flowchart TD
    CSV["pairs.csv<br/>90 rows: aadhaar,selfie"]
    PARSE["Parse CSV rows"]
    
    MODE{"Parallel<br/>mode?"}
    
    subgraph SERIAL["Serial Processing"]
        S_LOOP["For each pair:<br/>pipeline.run()"]
    end
    
    subgraph PARALLEL["Parallel Processing"]
        POOL["ThreadPoolExecutor<br/>max_workers=2"]
        T1["Thread 1:<br/>pipeline.run()"]
        T2["Thread 2:<br/>pipeline.run()"]
        TN["Thread N..."]
    end

    RESULTS["Collect results<br/>(sorted by original order)"]
    SUMMARY["write_batch_summary()<br/>summary.txt"]
    README["write_batch_readme()<br/>README.md with table"]
    PRINT["Print: 9/90 matches"]

    CSV --> PARSE --> MODE
    MODE -->|No| SERIAL --> RESULTS
    MODE -->|Yes| PARALLEL
    POOL --> T1 & T2 & TN
    T1 & T2 & TN --> RESULTS
    RESULTS --> SUMMARY & README --> PRINT
```

## Cache Strategy

```mermaid
flowchart TD
    INPUT["Image bytes"]
    HASH["SHA-256 hash"]
    LOOKUP{"Key in LRU<br/>cache?"}
    
    HIT["CACHE HIT<br/>Return stored FaceResult<br/>(skip detection + embedding)"]
    MISS["CACHE MISS<br/>Full processing pipeline"]
    STORE["Store in cache<br/>(LRU eviction if full)"]

    INPUT --> HASH --> LOOKUP
    LOOKUP -->|Yes| HIT
    LOOKUP -->|No| MISS --> STORE

    style HIT fill:#2d6a2d,color:#fff
    style MISS fill:#c0392b,color:#fff
```

## Age Gap Threshold Relaxation

```mermaid
flowchart TD
    AGE["Detected ages:<br/>Aadhaar vs Selfie"]
    GAP["age_gap = |age_a - age_s|"]
    
    CHECK{"gap > 5 years?"}
    NORELAX["No relaxation<br/>match_threshold = 0.60"]
    
    CALC["relaxation = (gap - 5) * 0.01<br/>capped at 0.10"]
    APPLY["new_threshold = 0.60 - relaxation<br/>minimum = 0.50"]
    
    EX1["Gap = 3yr -> threshold = 0.60"]
    EX2["Gap = 8yr -> threshold = 0.57"]
    EX3["Gap = 15yr -> threshold = 0.50"]
    EX4["Gap = 40yr -> threshold = 0.50 (capped)"]

    AGE --> GAP --> CHECK
    CHECK -->|No| NORELAX
    CHECK -->|Yes| CALC --> APPLY
    
    APPLY --> EX1 & EX2 & EX3 & EX4

    style EX1 fill:#2c3e50,color:#fff
    style EX2 fill:#2c3e50,color:#fff
    style EX3 fill:#2c3e50,color:#fff
    style EX4 fill:#2c3e50,color:#fff
```

## Configuration Sections

```mermaid
mindmap
  root((config.yaml))
    enhancement
      enabled: true
      model: RealESRGAN_x4plus
      upscale: 2
      quality_threshold: 0.4
    face
      model_pack: buffalo_l
      det_size: 640x640
      det_thresh: 0.7
      det_thresh_fallback: 0.5
      flip_augment: true
    similarity
      match_threshold: 0.60
      uncertain_low: 0.40
      adaptive_thresholds: false
      quality_weighted_fusion: false
    vlm_guard
      enabled: true
      model: qwen2.5vl:7b
      ollama_url: localhost:11434
      timeout_s: 300
    preprocessing
      aadhaar_clahe: true
      dual_path: true
      grayscale_normalize: false
    confidence_adjustments
      vlm_confirm_bonus: +8
      vlm_reject_high: -20
      vlm_reject_uncertain: -10
      quality_penalty: -5
      age_gap_bonus: +5
    Optional Modules
      adaface: disabled
      score_norm: disabled
      calibration: disabled
      crop_restore: disabled
      cache: max_size 64
      batch: serial mode
```

## File Map

```mermaid
flowchart TD
    subgraph ROOT["Project Root"]
        MAIN["main.py<br/>CLI entry point"]
        CONFIG["config.yaml<br/>All parameters"]
        PAIRS["pairs.csv<br/>90 test pairs"]
        CLAUDE["CLAUDE.md<br/>Project docs"]
    end

    subgraph PIPE["pipeline/"]
        ORCH["orchestrator.py<br/>Master pipeline"]
        ENH["enhancement.py<br/>Real-ESRGAN"]
        FP["face_processor.py<br/>InsightFace"]
        SIM["similarity.py<br/>Multi-metric scoring"]
        VLMG["vlm_guard.py<br/>Ollama VLM"]
        SNORM["score_norm.py<br/>S-norm calibration"]
        CCAL["confidence_calibrator.py<br/>Platt scaling"]
        CROPR["crop_restore.py<br/>Face denoising"]
        ADAF["adaface.py<br/>Second model"]
    end

    subgraph UTIL["utils/"]
        IMGU["image_utils.py<br/>I/O + preprocessing"]
        CFGL["config_loader.py<br/>YAML validation"]
        RESL["result_logger.py<br/>Logging + reports"]
        EMBC["embedding_cache.py<br/>LRU cache"]
        EXCP["exceptions.py<br/>Custom errors"]
    end

    subgraph TEST["tests/ (241 tests)"]
        T1["test_similarity.py (43)"]
        T2["test_new_features.py (36)"]
        T3["test_orchestrator_unit.py (33)"]
        T4["test_image_utils.py (31)"]
        T5["test_vlm_guard.py (25)"]
        T6["test_config_loader.py (24)"]
        T7["test_face_processor.py (15)"]
        T8["test_enhancement.py (15)"]
        T9["test_result_logger.py (11)"]
        T10["test_batch_logging.py (8)"]
    end

    subgraph DATA["FILES/"]
        AAD["AADHAR/<br/>9 cards (4 JPG + 5 PDF)"]
        SEL["SELFIE/<br/>10 photos (JPG)"]
    end

    MAIN --> ORCH
    ORCH --> ENH & FP & SIM & VLMG & SNORM & CCAL & CROPR & ADAF
    ORCH --> IMGU & EMBC
    MAIN --> CFGL & RESL
```
