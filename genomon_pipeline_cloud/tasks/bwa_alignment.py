#! /usr/bin/env python

import os
import pkg_resources
from ..abstract_task import *

class Bwa_alignment(Abstract_task):

    task_name = "bwa-alignment"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        super(Bwa_alignment, self).__init__(
            pkg_resources.resource_filename("genomon_pipeline_cloud", "script/{}.sh".format(self.__class__.task_name)),
            param_conf.get("bwa_alignment", "image"),
            param_conf.get("bwa_alignment", "resource"),
            output_dir + "/logging")

        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf, run_conf)


    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        # generate star_alignment_tasks.tsv
        #task_file = "{}/{}-tasks.tsv".format(task_dir, self.__class__.task_name)
        task_file = "{}/{}-tasks-{}-{}.tsv".format(task_dir, self.__class__.task_name, run_conf.get_owner_info(), run_conf.analysis_timestamp)
        with open(task_file, 'w') as hout:

            print >> hout, '\t'.join(["--env SAMPLE",
                                      "--input INPUT_BAM",
                                      "--input FASTQ1",
                                      "--input FASTQ2",
                                      "--output-recursive OUTPUT_DIR",
                                      "--input-recursive REFERENCE",
                                      "--env BAMTOFASTQ_OPTION",
                                      "--env BWA_OPTION",
                                      "--env BAMSORT_OPTION",
                                      "--env BAMMARKDUP_OPTION"])

            for sample in sample_conf.fastq:
                print >> hout, '\t'.join([sample,
                                          '',
                                          sample_conf.fastq[sample][0][0],
                                          sample_conf.fastq[sample][1][0],
                                          output_dir + "/bam/" + sample,
                                          param_conf.get("bwa_alignment", "bwa_reference"),
                                          '',
                                          param_conf.get("bwa_alignment", "bwa_option"),
                                          param_conf.get("bwa_alignment", "bamsort_option"),
                                          param_conf.get("bwa_alignment", "bammarkduplicates_option")])

            for sample in sample_conf.bam_tofastq:
                print >> hout, '\t'.join([sample,
                                          sample_conf.bam_tofastq[sample],
                                          '',
                                          '',
                                          output_dir + "/bam/" + sample,
                                          param_conf.get("bwa_alignment", "bwa_reference"),
                                          param_conf.get("bwa_alignment", "bamtofastq_option"),
                                          param_conf.get("bwa_alignment", "bwa_option"),
                                          param_conf.get("bwa_alignment", "bamsort_option"),
                                          param_conf.get("bwa_alignment", "bammarkduplicates_option")])

        return task_file
