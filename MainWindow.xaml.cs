using System;
using System.Collections.Generic;
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

        string connectionStr;

        public MainWindow() {
            InitializeComponent();
            connectionStr = Properties.Settings.Default.stackoverflowConnectionString;
        }

        private void Window_Loaded(object sender, RoutedEventArgs e) {
            string sql = "SELECT * FROM users";
            SqlConnection connection = null;
            try {
                connection = new SqlConnection(connectionStr);
                SqlCommand cmd = new SqlCommand(sql, connection);
                connection.Open();
                SqlDataReader reader = cmd.ExecuteReader();
                reader.Read();
                //MessageBox.Show(reader["display_name"].ToString());
            } catch (Exception ex) {
                MessageBox.Show(ex.Message);
            } finally {
                if (connection != null)
                    connection.Close();
            }
        }
    }
}
