# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "7b1741d0-647b-401a-9035-7f55da48199b",
# META       "default_lakehouse_name": "Unified",
# META       "default_lakehouse_workspace_id": "4c33a979-76f8-49c4-b2d6-fd32e4d5648e",
# META       "known_lakehouses": [
# META         {
# META           "id": "7b1741d0-647b-401a-9035-7f55da48199b"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

%run Util_Shared

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import col, expr, date_format, array_distinct, collect_list, lit, when
from datetime import datetime, timedelta
from azureml.opendatasets import PublicHolidays

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Define date range
current_date = datetime.today().replace(day=1)  # Set to first of the month
start_date = datetime(current_date.year - 2, 1, 1)  # January 1 of two years ago
end_date = datetime(2025, 12, 31)  # End of 2025

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Generate a date sequence using Spark
num_days = (end_date - start_date).days + 1
date_df = spark.range(num_days).withColumn("id", col("id").cast("int"))
date_df = date_df.selectExpr(f"date_add('{start_date.date()}', id) as calendar_date")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Load public holidays dataset
holidays = PublicHolidays().to_spark_dataframe()
holidays = holidays.filter(col("CountryRegion").isin(params["included_countries"]))
holidays = holidays.select(col("HolidayDate").alias("calendar_date"), col("HolidayName"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Aggregate holidays per date
holidays_grouped = holidays.groupBy("calendar_date").agg(
    array_distinct(collect_list("HolidayName")).alias("holidays"),
    lit(True).alias("International_Holiday")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create the calendar table
calendar_df = (date_df
    .withColumn("month_name", date_format(col("calendar_date"), "MMMM"))
    .withColumn("year", date_format(col("calendar_date"), "yyyy"))
    .withColumn("relative_month", expr(f"(year(calendar_date) - year(current_date)) * 12 + (month(calendar_date) - month(current_date))"))
    .join(holidays_grouped, "calendar_date", "left")
    .withColumn("holidays", when(col("holidays").isNotNull(), col("holidays")).otherwise(lit([])))
    .withColumn("HolidayFlag", when(col("HolidayFlag").isNotNull(), col("HolidayFlag")).otherwise(lit(False)))
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

calendar_df.write.mode("overwrite").format("delta").option("overwriteSchema", "true").save("Tables/Dataprod/DIM_Calendar")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
