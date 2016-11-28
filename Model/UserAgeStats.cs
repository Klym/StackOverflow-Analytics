using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using LiveCharts;

namespace StackOverflow_Analytics {
    public class UserAgeStats : StatsModel {

        public UserAgeStats(int from, int to) {
            string query = "select Count(users.id) as cnt from users where age between " + from + " and " + to;
            this.Values = new ChartValues<int>();
            this.select(query);
        }

        protected override void parseReader(SqlDataReader reader) {
            while(reader.Read()) {
                this.Values.Add(int.Parse(reader["cnt"].ToString()));
            }
        }
    }
}
