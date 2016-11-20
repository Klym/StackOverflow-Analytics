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

namespace StackOverflow_Analytics {
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window {

        public MainWindow() {
            InitializeComponent();
        }

        private void Window_Loaded(object sender, RoutedEventArgs e) {
            QuestionsViewModel questionVM = new QuestionsViewModel();
            DataContext = questionVM;
            MainFrame.NavigationUIVisibility = NavigationUIVisibility.Hidden;
        }

        private void Expander_MouseDoubleClick(object sender, MouseButtonEventArgs e) {            
            MainFrame.Navigate(new QuestionsListPage());
        }

        private void Expander_MouseDoubleClick_1(object sender, MouseButtonEventArgs e) {
            MainFrame.Navigate(new UsersListPage());
        }

        private void Expander_MouseDoubleClick_2(object sender, MouseButtonEventArgs e) {
            MainFrame.Navigate(new TagsListPage());
        }

        private void Button_MouseDoubleClick(object sender, MouseButtonEventArgs e) {
            MainFrame.Navigate(new TechStatsPage());
        }

        private void Button_MouseDoubleClick_1(object sender, MouseButtonEventArgs e) {
            MainFrame.Navigate(new UserAgeStatsPage());
        }
    }
}
