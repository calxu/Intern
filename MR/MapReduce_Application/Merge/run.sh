#!/bin/bash
# Author: Calvin,Xu

HADOOP_BIN="/home/`whoami`/bin/hadoop"

INPUT1="/201705/*"
INPUT2="/201706/*"
INPUT3="/201707/*"

#输出目录，path必须不存在
HADOOP_OUTPUT="/Merge"

TASK_NAME="Task"
${HADOOP_BIN} fs -test -e ${HADOOP_OUTPUT}
if [ $? -eq 0 ]; then
    ${HADOOP_BIN} fs -rmr ${HADOOP_OUTPUT}
fi
# 用来指定分桶时,按照分隔符切割后,用于分桶key所占的列数
# 设置map程序分隔符的位置,该位置之前的部分作为key,之后的部分作为value
$HADOOP_BIN streaming \
    -D mapred.job.map.capacity=10000 \
    -D mapred.job.reduce.capacity=1000 \
    -D num.key.fields.for.partition=1 \
    -D stream.num.map.output.key.fields=1 \
    -D stream.memory.limit=30000 \
    -D mapred.task.hce.accept.limit=300000 \
    -D mapred.hce.replace.streaming=false \
    -D mapred.job.priority="VERY_HIGH" \
    -D mapred.job.name="${TASK_NAME}" \
    -D mapred.map.tasks=1000 \
    -D mapred.reduce.tasks=100 \
    -input ${INPUT1} \
    -input ${INPUT2} \
    -input ${INPUT3} \
    -output ${HADOOP_OUTPUT} \
    -mapper "mapper.py" \
    -reducer "reducer.py" \
    -file "mapper.py" \
    -file "reducer.py" \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
