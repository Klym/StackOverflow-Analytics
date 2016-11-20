using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;
using LiveCharts;

namespace StackOverflow_Analytics {
    public class TechStats : StatsModel {
        public string Name { get; set; }
        public ChartValues<int> Values { get; set; }

        public TechStats(string name) {
            this.Name = name;
            this.Values = new ChartValues<int>();
            string query = "select Count(questions.id) as cnt, datepart(yyyy, questions.creation_date) as year from q_tags join tags on tag_id = id join questions on questions.id = question_id where name = '" + this.Name + "' group by datepart(yyyy, questions.[creation_date]) order by year";
            this.select(query);
        }

        protected override void parseReader(SqlDataReader reader) {
            while (reader.Read()) {
                this.Values.Add(int.Parse(reader["cnt"].ToString()));
            }
        }
    }
}