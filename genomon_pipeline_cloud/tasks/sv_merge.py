#! /usr/bin/env python

import pkg_resources
from ..abstract_task import *
 
class SV_merge(Abstract_task):

    task_name = "sv-merge"

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        super(SV_merge, self).__init__(
            pkg_resources.resource_filename("genomon_pipeline_cloud", "script/{}.sh".format(self.__class__.task_name)),
            param_conf.get("sv_merge", "image"),
            param_conf.get("sv_merge", "resource"),
            output_dir + "/logging")
        
        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf, run_conf)


    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        task_file = "{}/{}-tasks-{}-{}.tsv".format(task_dir, self.__class__.task_name, run_conf.get_owner_info(), run_conf.analysis_timestamp)
        with open(task_file, 'w') as hout:

            # List up the sample list
            control_panel_list_for_merge = []
            for tumor_sample, normal_sample, control_panel_name in sample_conf.sv_detection:
                control_panel_list_for_merge.append(control_panel_name)
            control_panel_list_uniq = list(set(control_panel_list_for_merge))

            # Get max count of samples
            max_count = 0
            for panel_name in sample_conf.control_panel:
                if panel_name in control_panel_list_uniq:
                    count_sample = len(sample_conf.control_panel[panel_name])
                    if max_count < count_sample:
                        max_count = count_sample

            header_li = ["--env PANEL_NAME",
                         "--output-recursive OUTPUT_DIR",
                         "--env META",
                         "--env MAX_COUNT",
                         "--env OPTION"]

            for cnt in range(1, max_count+1):
                header_li.append("--input-recursive INPUT_DIR_" + str(cnt))
            
            print >> hout, '\t'.join(header_li)

            for panel_name in sample_conf.control_panel:
                if panel_name in control_panel_list_uniq:

                    record = [panel_name,
                              output_dir + "/sv/control_panel/" + panel_name,
                              run_conf.get_meta_info(param_conf.get("sv_merge", "image")),
                              str(max_count),
                              param_conf.get("sv_merge", "genomon_sv_merge_option")]

                    for sample in sample_conf.control_panel[panel_name]:
                        record.append(output_dir + "/sv/" + sample)

                    for cnt in range(len(sample_conf.control_panel[panel_name]), max_count):
                        record.append("")
            
                    print >> hout, '\t'.join(record)

        return task_file

