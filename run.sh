#!/bin/bash

HADOOP_BIN="/home/hadoop/bin/hadoop"

INPUT1="table2"

INPUT2="table1"

#输出目录，path必须不存在
HADOOP_OUTPUT="temporary_result"

TASK_NAME="COUNT IDM"
${HADOOP_BIN} fs -test -e ${HADOOP_OUTPUT}
if [ $? -eq 0 ]; then
    ${HADOOP_BIN} fs -rmr ${HADOOP_OUTPUT}
fi
# 设备号类别 3:CUID 4:IMEI 12:MAC 15:IDFA
echo 'start'
echo ${HADOOP_OUTPUT}
# 用来指定分桶时,按照分隔符切割后,用于分桶key所占的列数
# 设置map程序分隔符的位置,该位置之前的部分作为key,之后的部分作为value
$HADOOP_BIN streaming \
    -D mapred.job.map.capacity=1000 \
    -D mapred.job.reduce.capacity=100 \
    -D num.key.fields.for.partition=1 \
    -D stream.num.map.output.key.fields=1 \
    -D mapred.task.hce.accept.limit=30000 \
    -D mapred.job.priority="VERY_HIGH" \
    -D mapred.job.name="${TASK_NAME}" \
    -D mapred.map.tasks=1000 \
    -D mapred.reduce.tasks=100 \
    -input ${INPUT1} \
    -input ${INPUT2} \
    -output ${HADOOP_OUTPUT} \
    -mapper "mapper.py" \
    -reducer "reducer.py" \
    -file "mapper.py" \
    -file "reducer.py" \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
#
if [[ $? -eq 0 ]];then
    echo ${HADOOP_OUTPUT}
    echo 'OK'
else
    echo 'FAILED'
    exit 1
fi


OUTPUT="temporary_result"
$HADOOP_BIN fs -cat ${OUTPUT} | awk '{sum1+=$2}END{print sum1}'
