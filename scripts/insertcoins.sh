#!/bin/bash
mysql -uroot -pc0mm0ns "wp-donationbox" < "insert_05EUR.sql"
sleep 1
mysql -uroot -pc0mm0ns "wp-donationbox" < "insert_1EUR.sql"
sleep 1
mysql -uroot -pc0mm0ns "wp-donationbox" < "insert_2EUR.sql"
