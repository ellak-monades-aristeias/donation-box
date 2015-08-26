#!/bin/bash
mysql -uroot -pc0mm0ns "wp-donationbox" < "truncate_coins.sql"
mysql -uroot -pc0mm0ns "wp-donationbox" < "truncate_donations.sql"
