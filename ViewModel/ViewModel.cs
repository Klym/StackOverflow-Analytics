using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;

namespace StackOverflow_Analytics {
    public abstract class ViewModel {

        protected string connectionString = Properties.Settings.Default.stackoverflowConnectionString;

        protected abstract void createObject(SqlDataReader reader);

        protected void selectData(string query) {
            SqlConnection connection = null;
            SqlDataReader reader = null;
            try {
                connection = new SqlConnection(connectionString);
                SqlCommand cmd = new SqlCommand(query, connection);
                connection.Open();
                reader = cmd.ExecuteReader();
                this.createObject(reader);
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
