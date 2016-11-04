using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StackOverflow_Analytics {
    public class Question {
        public int Id { get; set; }
        public string UserName { get; set; }
        public string Title { get; set; }
        public string Body { get; set; }
        public bool IsAnswerd { get; set; }
        public int AnswerCount { get; set; }
        public int ViewCount { get; set; }
        public int Score { get; set; }
        public int UpVoteCount { get; set; }
        public DateTime CreationDate { get; set; }

        public Question(int id, string user, string title, string body, bool isAnswerd, int aCnt, int vCnt, int score, int upCnt, string date) {
            this.Id = id;
            this.UserName = user;
            this.Title = title;
            this.Body = body;
            this.IsAnswerd = isAnswerd;
            this.AnswerCount = aCnt;
            this.ViewCount = vCnt;
            this.Score = score;
            this.UpVoteCount = UpVoteCount;
            string[] parseDate = date.Split('-');
            this.CreationDate = new DateTime(int.Parse(parseDate[0]), int.Parse(parseDate[1]), int.Parse(parseDate[2]));
        }
    }
}
