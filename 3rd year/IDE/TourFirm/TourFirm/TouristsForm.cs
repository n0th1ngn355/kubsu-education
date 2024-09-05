using Npgsql;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace TourFirm
{
    public partial class TouristsForm : Form
    {
        private string connectionString = "Host=localhost;Username=postgres;Password=postgres;Database=Tourfirm";

        public int row_id;
        public string row_name;

        public Dictionary<string, int> d;

        public TouristsForm()
        {
            InitializeComponent();
        }

        protected override void OnLoad(EventArgs e)
        {
            base.OnLoad(e);
            using (var connection = new NpgsqlConnection(connectionString))
            {
                connection.Open();

                DataTable schema = connection.GetSchema("Tables");

                foreach (DataRow row in schema.Rows)
                {
                    string tableName = row["TABLE_NAME"].ToString();
                    comboBoxTables.Items.Add(tableName);
                }
                comboBoxTables.SelectedIndex = 0;
            }
            LoadFields(comboBoxTables.SelectedItem.ToString());
        }


        private void comboBoxTables_SelectedIndexChanged(object sender, EventArgs e)
        {
            string selectedTable = comboBoxTables.SelectedItem.ToString();
            
            LoadFields(selectedTable);
        }

        private void updateData(string tableName, NpgsqlConnection connection)
        {
            DataTable dt1 = new DataTable();
            NpgsqlDataAdapter adap1 = new NpgsqlDataAdapter("SELECT * FROM " + tableName, connection);
            adap1.Fill(dt1);
            dataGridView1.DataSource = dt1;
            dataGridView1.ClearSelection();

            row_name = dataGridView1.Columns[0].Name;
            d = new Dictionary<string, int>();
            for (int i = 0; i < dataGridView1.Columns.Count; i++)
            {
                d[dataGridView1.Columns[i].Name] = i;
                //Console.WriteLine(dataGridView1.Columns[i].Name + " " +  i);
                //Console.WriteLine(d[dataGridView1.Columns[i].Name]);
            }
        }

        private void LoadFields(string tableName)
        {
            flowLayoutPanelFields.Controls.Clear();

            using (var connection = new NpgsqlConnection(connectionString))
            {
                connection.Open();

                updateData(tableName, connection);

                string query = $"SELECT column_name FROM information_schema.columns WHERE table_name = '{tableName}'";

                using (var command = new NpgsqlCommand(query, connection))
                {
                    using (var reader = command.ExecuteReader())
                    {
                        reader.Read();
                        while (reader.Read())
                        {
                            string columnName = reader.GetString(0);

                            Label label = new Label();
                            label.Text = columnName + ":";
                            label.AutoSize = true;

                            TextBox textBox = new TextBox();
                            textBox.Name = columnName;

                            flowLayoutPanelFields.Controls.Add(label);
                            flowLayoutPanelFields.Controls.Add(textBox);
                        }
                    }
                }
            }
        }

        public void getData(ref string columns,ref string values)
        {
            // Генерация строк для столбцов и значений на основе введенных данных
            foreach (Control control in flowLayoutPanelFields.Controls)
            {
                if (control is TextBox)
                {
                    columns += ((TextBox)control).Name + ",";
                    values += "'" + ((TextBox)control).Text + "',";
                }
            }
            columns = columns.TrimEnd(',');
            values = values.TrimEnd(',');
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string selectedTable = comboBoxTables.SelectedItem.ToString();

            string columns = "";
            string values = "";

            getData(ref columns, ref values);

            using (var conn = new NpgsqlConnection(connectionString))
            {
                try
                {
                    conn.Open();

                    // Формирование SQL-запроса на вставку данных в выбранную таблицу
                    string query = $"INSERT INTO {selectedTable} ({columns}) VALUES ({values});";
                    //Console.WriteLine(query);
                    // Выполнение запроса
                    using (var cmd = new NpgsqlCommand(query, conn))
                    {
                        cmd.ExecuteNonQuery();
                    }

                    MessageBox.Show("Data saved successfully!");
                    updateData(selectedTable, conn);
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Error: " + ex.Message);
                }
            }
        }

        private void dataGridView1_SelectionChanged(object sender, EventArgs e)
        {
            var a = ((DataGridView)sender).SelectedRows;
            if (a.Count > 0)
            {
                row_id = Int32.Parse(a[0].Cells[0].Value.ToString());
                for (int i = 0; i < flowLayoutPanelFields.Controls.Count/2; i++)
                {
                    var lb = flowLayoutPanelFields.Controls[i*2];
                    var tb = flowLayoutPanelFields.Controls[i*2+1];
                    var temp = lb.Text.Substring(0,lb.Text.Length-1);
                    tb.Text = a[0].Cells[d[temp]].Value.ToString();
                }
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            if(dataGridView1.SelectedRows.Count > 0)
            {
                string selectedTable = comboBoxTables.SelectedItem.ToString();
                string columns = "";
                string values = "";

                getData(ref columns, ref values);

                var colList = columns.Split(',');
                var valList = values.Split(',');

                using (var conn = new NpgsqlConnection(connectionString))
                {
                    try
                    {
                        conn.Open();

                        // Формирование SQL-запроса на вставку данных в выбранную таблицу
                        List<string> strings = new List<string>();
                        for (int i = 0; i < colList.Count(); i++)
                        {
                            strings.Add($"{colList[i]} = {valList[0]}");
                        }
                        var upd = String.Join(", ", strings);

                        string query = $"UPDATE {selectedTable} SET {upd} WHERE {row_name}={row_id};";
                        Console.WriteLine(query);
                        // Выполнение запроса
                        using (var cmd = new NpgsqlCommand(query, conn))
                        {
                            cmd.ExecuteNonQuery();
                        }

                        MessageBox.Show("Data saved successfully!");
                        updateData(selectedTable, conn);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show("Error: " + ex.Message);
                    }
                }

            }
        }
    }
}
