using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;

namespace StackOverflow_Analytics {
    public class Question {
        public int Id { get; set; }
        public string UserName { get; set; }
        public string Title { get; set; }
        public string Body { get; set; }
        public bool IsAnswered { get; set; }
        public int AnswerCount { get; set; }
        public int ViewCount { get; set; }
        public int Score { get; set; }
        public int UpVoteCount { get; set; }
        public DateTime CreationDate { get; set; }
        public string DateString { get; set; }
        public ObservableCollection<Tag> Tags { get; }

        public Question(string id, string user, string title, string body, string isAnswered, string aCnt, string vCnt, string score, string upCnt, string date) {
            this.Id = int.Parse(id);
            this.UserName = user;
            this.Title = title;
            this.Body = body;
            this.IsAnswered = bool.Parse(isAnswered);
            this.AnswerCount = int.Parse(aCnt);
            this.ViewCount = int.Parse(vCnt);
            this.Score = int.Parse(score);
            this.UpVoteCount = int.Parse(upCnt);
            string[] parseDate = date.Split('.');
            this.CreationDate = new DateTime(int.Parse(parseDate[2].Substring(0, parseDate[2].IndexOf(' '))), int.Parse(parseDate[1]), int.Parse(parseDate[0]));
            this.DateString = this.CreationDate.ToString("dd.MM.yyyy");
            this.Tags = new ObservableCollection<Tag>();
            this.getTags();
        }

        public void getTags() {
            string sql = "SELECT * FROM q_tags JOIN tags ON id = tag_id WHERE question_id=" + this.Id;
            SqlConnection connection = null;
            SqlDataReader reader = null;
            try {
                connection = new SqlConnection(Properties.Settings.Default.stackoverflowConnectionString);
                SqlCommand cmd = new SqlCommand(sql, connection);
                connection.Open();
                reader = cmd.ExecuteReader();
                while (reader.Read()) {
                    this.Tags.Add(new Tag(reader["id"].ToString(), reader["name"].ToString(), reader["count"].ToString(), reader["has_synonyms"].ToString()));
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
    }
}
