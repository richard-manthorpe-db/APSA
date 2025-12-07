try:

	from airflow import DAG
	from datetime import datetime
	print("All modules are ok")
except Exception as e:
	print("Error {}".format(e))

