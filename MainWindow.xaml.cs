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
using LiveCharts;
using LiveCharts.Wpf;

namespace StackOverflow_Analytics {
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window {

        public TechStatsPage statsPage { get; set; }
        public QuestionsViewModel questionVM { get; set; }
        public TagsViewModel tagsVM { get; set; }

        public MainWindow() {
            InitializeComponent();
            statsPage = new TechStatsPage();
        }

        private void Window_Loaded(object sender, RoutedEventArgs e) {
            questionVM = new QuestionsViewModel();
            MainFrame.NavigationUIVisibility = NavigationUIVisibility.Hidden;
            tagsVM = new TagsViewModel();
            tagsVM.getTopTags();

            string[] technologies = new string[] { "c#", "c++", "java", "python", "php", "javascript" };
            for (int i = 0; i < technologies.Length; i++) {
                techsList.Items.Add(technologies[i]);
            }

            DataContext = this;
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
            MainFrame.Navigate(statsPage);
        }

        private void Button_MouseDoubleClick_1(object sender, MouseButtonEventArgs e) {
            MainFrame.Navigate(new UserAgeStatsPage());
        }

        private void Button_Click(object sender, RoutedEventArgs e) {
            Tag tag = (Tag)allTechsList.SelectedItem;
            if (techsList.Items.IndexOf(tag.Name) != -1) return;
            techsList.Items.Add(tag.Name);
            TechStats stat = new TechStats(tag.Name);
            statsPage.SeriesCollection.Add(new LineSeries {
                Title = tag.Name,
                Values = stat.Values,
            });
        }

        private void Button_Click_1(object sender, RoutedEventArgs e) {
            if (techsList.SelectedIndex == -1) return;
            statsPage.SeriesCollection.RemoveAt(techsList.SelectedIndex);
            techsList.Items.RemoveAt(techsList.SelectedIndex);
        }
    }
}
