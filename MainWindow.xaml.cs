using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Data.SqlClient;
using System.Data;
using System.Configuration;

namespace StackOverflow_Analytics {
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window {

        public string connectionStr;
        public ObservableCollection<Question> Questions { get; set; }

        public MainWindow() {
            InitializeComponent();
            connectionStr = Properties.Settings.Default.stackoverflowConnectionString;
        }

        private void Window_Loaded(object sender, RoutedEventArgs e) {
            string sql = "SELECT questions.*, users.display_name AS u_name FROM questions JOIN users ON user_id = users.id ORDER BY score DESC";
            SqlConnection connection = null;
            SqlDataReader reader = null;
            try {
                connection = new SqlConnection(connectionStr);
                SqlCommand cmd = new SqlCommand(sql, connection);
                connection.Open();
                reader = cmd.ExecuteReader();
                Questions = new ObservableCollection<Question>();
                while (reader.Read()) {
                    Questions.Add(new Question(reader["id"].ToString(), reader["u_name"].ToString(), reader["title"].ToString(), reader["body"].ToString(), "false", reader["answer_count"].ToString(), reader["view_count"].ToString(), reader["score"].ToString(), reader["up_vote_count"].ToString(), reader["creation_date"].ToString()));
                }
                questionsList.Items.Clear();
                questionsList.ItemsSource = Questions;
            } catch (Exception ex) {
                MessageBox.Show(ex.Message);
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
