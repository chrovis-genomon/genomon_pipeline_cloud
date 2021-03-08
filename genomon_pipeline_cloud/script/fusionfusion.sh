#!/bin/bash

set -o errexit
set -o xtrace

INPUT_PREF=${INPUT_DIR}/${SAMPLE}
OUTPUT_PREF=${OUTPUT_DIR}/${SAMPLE}
mkdir -p ${OUTPUT_DIR}

if [ "_${MERGED_COUNT_DIR}" != "_" ]; then
    OPTION="${OPTION} --pooled_control_file ${MERGED_COUNT_DIR}/${PANEL_NAME}.merged.Chimeric.count"
fi
/usr/local/bin/fusionfusion \
  --star ${INPUT_PREF}.Chimeric.out.sam \
  --star_sj_tab ${INPUT_PREF}.SJ.out.tab \
  --star_aligned_bam ${INPUT_PREF}.Aligned.sortedByCoord.out.bam \
  --out ${OUTPUT_DIR} \
  --reference_genome ${REFERENCE} \
  ${OPTION}

mv ${OUTPUT_DIR}/star.fusion.result.txt ${OUTPUT_DIR}/${SAMPLE}.star.fusion.result.txt
mv ${OUTPUT_DIR}/fusion_fusion.result.txt ${OUTPUT_DIR}/${SAMPLE}.genomonFusion.result.txt
mv ${OUTPUT_DIR}/fusion_fusion.result.traced.txt ${OUTPUT_DIR}/${SAMPLE}.genomonFusion.result.traced.txt

/usr/local/bin/fusion_utils filt ${OUTPUT_DIR}/${SAMPLE}.genomonFusion.result.txt ${OUTPUT_DIR}/${SAMPLE}.fusion_fusion.result.filt.txt ${FILT_OPTION}

mv ${OUTPUT_DIR}/${SAMPLE}.fusion_fusion.result.filt.txt ${OUTPUT_DIR}/${SAMPLE}.genomonFusion.result.filt.txt

