
# -*- coding: utf-8 -*-

rm(list = ls())

# ADNIMERGE_18Feb2025.csv

# RID: 환자의 고유 식별 번호
# * COLPROT: ADNI 연구 프로토콜 정보; 데이터 획득 시점 (예: ADNI1, ADNI2)
# * ORIGPROT: ADNI 연구 프로토콜 정보; 연구 참여 시점 (예: ADNI1, ADNI2)
# * PTID: 환자 ID
# SITE: 연구 사이트 코드
# * VISCODE: 방문 코드 (예: bl = baseline, m06 = 6개월 후, m12 = 12개월 후); 반복 측정 데이터
# EXAMDATE: 검사 날짜
# * DX_bl: 초기 진단 정보 (예: CN = 정상, MCI = 경도인지장애, AD = 알츠하이머)
# * AGE: 나이
# * PTGENDER: 성별
# PTEDUCAT: 교육 연수
# PTETHCAT: 민족 범주
# PTRACCAT: 인종 범주
# PTMARRY: 결혼 상태
# * APOE4: APOE4 유전자 보유 여부 (0, 1, 2)
# FDG: FDG-PET (포도당 대사)
# PIB: 아밀로이드 PET 스캔 결과
# * AV45: 아밀로이드 PET 스캔 결과 (PIB, AV45, FBB 중 가장 많이 사용됨)
# FBB: 아밀로이드 PET 스캔 결과
# * ABETA: CSF or Plasma AD 바이오마커 (베타-아밀로이드)
# * TAU: CSF AD 바이오마커 (타우 단백질)
# * PTAU: CSF AD (알츠하이머 특이) 바이오마커 (타우 단백질)
# CDRSB: 임상치매등급(Clinical Dementia Rating Sum of Boxes)
# ADAS11: ADAS-Cog 인지 테스트 점수
# ADAS13: ADAS-Cog 인지 테스트 점수
# ADASQ4: ADAS-Cog 인지 테스트 점수
# RAVLT_immediate: 언어 기억력과 학습 능력을 평가 점수
# RAVLT_learning: 언어 기억력과 학습 능력을 평가 점수
# RAVLT_forgetting: 언어 기억력과 학습 능력을 평가 점수
# RAVLT_perc_forgetting: 언어 기억력과 학습 능력을 평가 점수
# LDELTOTAL: 알츠하이머병(AD) 및 경도인지장애(MCI) 환자들의 인지 기능 평가 점수
# DIGITSCOR: 알츠하이머병(AD) 및 경도인지장애(MCI) 환자들의 인지 기능 평가 점수
# TRABSCOR: 알츠하이머병(AD) 및 경도인지장애(MCI) 환자들의 인지 기능 평가 점수
# FAQ: Functional Activities Questionnaire (기능 평가)
# MOCA: 인지 기능을 전반적으로 평가하는 신경심리학적 검사 점수
# Ecog~: 일상생활에서의 인지 기능 평가 점수
# * FLDSTRENG: MRI 촬영에 사용된 자기장 세기(Tesla 단위)를 나타내는 변수 (같은 뇌 구조라도 1.5T와 3T에서 촬영된 영상은 차이가 날 수 있음)
# * FSVERSION: FreeSurfer 버전 (MRI 분석 소프트웨어)
# * IMAGEUID: MRI/PET 스캔 이미지 ID (DICOM/NIfTI 형식의 실제 뇌 영상 데이터와 매칭할 때 사용)
# * Ventricles: 뇌실 부피
# * Hippocampus: 해마 부피
# * WholeBrain: 전체 뇌 부피
# * Entorhinal: 내후각 피질 두께 혹은 부피 (AD 와 관계있음)
# * Fusiform: 방추상회 두께 혹은 부피 (AD 와 관계있음)
# * MidTemp: 중측두엽 두께 혹은 부피 (AD 와 관계있음)
# * ICV: 두개강 용적 (Intracranial Volume)
# * DX: 환자의 진단 상태를 나타냄 (CN (Cognitively Normal): 정상군 등 등)
# PCAA: 평가 점수
# * _bl: base line

library(readr)

adnimerge <- readr::read_csv(
    "./R/ADNIMERGE/IDA_ADNI/ADNIMERGE_18Feb2025.csv",
    col_types = cols(
        .default = col_double(),
        COLPROT = col_character(),
        ORIGPROT = col_character(),
        PTID = col_character(),
        VISCODE = col_character(),
        EXAMDATE = col_date(format = ""),
        DX_bl = col_character(),
        PTGENDER = col_character(),
        PTETHCAT = col_character(),
        PTRACCAT = col_character(),
        PTMARRY = col_character(),
        ABETA = col_character(),
        TAU = col_character(),
        PTAU = col_character(),
        FLDSTRENG = col_character(),
        FSVERSION = col_character(),
        DX = col_character(),
        EXAMDATE_bl = col_date(format = ""),
        FLDSTRENG_bl = col_character(),
        FSVERSION_bl = col_character(),
        ABETA_bl = col_character(),
        TAU_bl = col_character(),
        PTAU_bl = col_character(),
        update_stamp = col_datetime(format = "")
    )
)

head(adnimerge)
colnames(adnimerge)
