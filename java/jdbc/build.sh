#!/bin/bash
set -e
javac -cp /root/mysql-connector-java-5.1.47/mysql-connector-java-5.1.47.jar JDBCClient.java
java -Djava.ext.dirs=/root/mysql-connector-java-5.1.47 JDBCClient
