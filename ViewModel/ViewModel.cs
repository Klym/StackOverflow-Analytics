using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;

namespace StackOverflow_Analytics {
    public abstract class ViewModel {

        public ObservableCollection<IModel> Data { get; set; }
        protected string connectionString = Properties.Settings.Default.stackoverflowConnectionString;
        protected abstract IModel createObject(SqlDataReader reader);

        public ViewModel() {
            this.Data = new ObservableCollection<IModel>();
        }

        protected void selectData(string query) {
            SqlConnection connection = null;
            SqlDataReader reader = null;
            try {
                connection = new SqlConnection(connectionString);
                SqlCommand cmd = new SqlCommand(query, connection);
                connection.Open();
                reader = cmd.ExecuteReader();
                while (reader.Read()) {
                    IModel item = this.createObject(reader);
                    this.Data.Add(item);
                }
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

        public static DateTime strToDateTime(string date) {
            string[] parseDate = date.Split('.');
            return new DateTime(int.Parse(parseDate[2].Substring(0, parseDate[2].IndexOf(' '))), int.Parse(parseDate[1]), int.Parse(parseDate[0]));
        }
    }
}