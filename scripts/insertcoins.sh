#!/bin/bash
mysql -uroot -pc0mm0ns "wordpress" < "insert_05EUR.sql"
sleep 1
mysql -uroot -pc0mm0ns "wordpress" < "insert_1EUR.sql"
sleep 1
mysql -uroot -pc0mm0ns "wordpress" < "insert_2EUR.sql"
