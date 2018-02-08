rm *.log

select_path=.........
PROJECT_HOME=............
tf_input=${select_path}
output_path="${PROJECT_HOME}/tfrecord_haha"
hadoop fs -test -e ${output_path} 
if [ $? -eq 0 ];then
    hadoop fs -rm -r ${output_path}
fi
tf_save_path="hdfs://ns3${PROJECT_HOME}/save_tfrecord"
hadoop fs -rmr ${tf_save_path}
hadoop fs -mkdir ${tf_save_path}

hadoop jar /hadoop_path..../share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar  \
        -D mapred.job.priority=HIGH \
        -D mapred.job.name="tfrecord" \
        -D mapred.map.tasks=200 \
        -D mapred.reduce.tasks=200 \
        -D mapreduce.job.map.memory.mb=8000 \
        -D mapreduce.job.reduce.memory.mb=8000 \
        -cacheArchive "/hadoop_online_path..../anaconda2.tar.gz#py27" \
        -input "${tf_input}" \
        -output "${output_path}" \
        -file ./gen_tfrecord.py \
        -mapper "py27/anaconda2/bin/python2.7 gen_tfrecord.py mapper" \
        -reducer "py27/anaconda2/bin/python2.7 gen_tfrecord.py reducer ${tf_save_path}"  

echo "End"
