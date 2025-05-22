# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

prod_workspace_id = "736ca819-08eb-458a-96d4-78fd8145ea4e"
environment = "prod" if notebookutils.runtime.context["currentWorkspaceId"] == prod_workspace_id else "dev"

key_vault_url = f"https://helix-akv-{environment}.vault.azure.net/"
tenant_id = "72f988bf-86f1-41af-91ab-2d7cd011db47"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

client_id = notebookutils.credentials.getSecret(key_vault_url, "default_client_id")
client_secret = notebookutils.credentials.getSecret(key_vault_url, "default_client_secret")

spark.conf.set("fs.azure.account.auth.type", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id", client_id)
spark.conf.set("fs.azure.account.oauth2.client.secret", client_secret)
spark.conf.set("fs.azure.account.oauth2.client.endpoint", tenant_id)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

connection = {
    "unified_default": f"abfss://Helix-{environment}-Storage@dxt-onelake.dfs.fabric.microsoft.com/Unified.Lakehouse/",
    "marketing_prod": "abfss://DEMO-SOURCE@dxt-onelake.dfs.fabric.microsoft.com/Marketing.Lakehouse/",
    "finance_prod": "abfss://DEMO-SOURCE@dxt-onelake.dfs.fabric.microsoft.com/Finance.Lakehouse/",
    "hr_prod": "abfss://DEMO-SOURCE@dxt-onelake.dfs.fabric.microsoft.com/HR.Lakehouse/",
    "nyc_prod": "abfss://DEMO-SOURCE@dxt-onelake.dfs.fabric.microsoft.com/NYC.Lakehouse/"
}

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
