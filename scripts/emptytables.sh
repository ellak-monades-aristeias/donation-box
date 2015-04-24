#!/bin/bash
mysql -uroot -pc0mm0ns "wordpress" < "truncate_coins.sql"
mysql -uroot -pc0mm0ns "wordpress" < "truncate_donations.sql"
