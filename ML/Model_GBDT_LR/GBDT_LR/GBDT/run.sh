#!/bin/bash

HADOOP_BIN="/home/`whoami`/bin/hadoop"

INPUT="Table1"
INPUT="Table2"
HADOOP_OUTPUT="Result"


# 用来指定分桶时,按照分隔符切割后,用于分桶key所占的列数
# 设置map程序分隔符的位置,该位置之前的部分作为key,之后的部分作为value
$HADOOP_BIN streaming \
    -D mapred.job.map.capacity=1000 \
    -D mapred.job.reduce.capacity=1000 \
    -D num.key.fields.for.partition=1 \
    -D stream.num.map.output.key.fields=1 \
    -D stream.memory.limit=10000 \
    -D mapred.task.hce.accept.limit=300000 \
    -D mapred.job.priority="VERY_HIGH" \
    -D mapred.job.name="Task" \
    -D mapred.map.tasks=1000 \
    -D mapred.reduce.tasks=40 \
    -D mapred.textoutputformat.ignoreseparator=true \
    -input ${INPUT} \
    -output ${HADOOP_OUTPUT} \
    -mapper "oneHot.py" \
    -reducer "reduce.py" \
    -file "oneHot.py" \
    -file "reduce.py" \
    -file "model_dump" \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
