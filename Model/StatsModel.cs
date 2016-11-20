using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;

namespace StackOverflow_Analytics {
    public abstract class StatsModel {

        protected abstract void parseReader(SqlDataReader reader);

        protected void select(string query) {
            SqlConnection connection = null;
            SqlDataReader reader = null;
            try {
                connection = new SqlConnection(Properties.Settings.Default.stackoverflowConnectionString);
                SqlCommand cmd = new SqlCommand(query, connection);
                connection.Open();
                reader = cmd.ExecuteReader();
                this.parseReader(reader);
            } catch (Exception ex) {
                throw new Exception(ex.Message);
            } finally {
                if (reader != null) {
                    reader.Close();
                }
                if (connection != null) {
                    connection.Close();
                }
            }
        }
    }
}
