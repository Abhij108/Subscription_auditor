import { useMemo } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

function Dashboard({ data }) {

  if (!data) {
    return (
      <div className="dashboard-empty">
        <h2>Subscription Auditor</h2>

        <p>
          Upload your bank statement to analyze
          recurring payments.
        </p>
      </div>
    );
  }

  const subscriptions = data.subscriptions || [];
  const transactions = data.transactions || [];

  const totalMonthly = useMemo(() => {

    return subscriptions.reduce(
      (total, item) =>
        total + Number(item.monthly_cost || 0),
      0
    );

  }, [subscriptions]);


  const totalAnnual = useMemo(() => {

    return subscriptions.reduce(
      (total, item) =>
        total + Number(item.annual_cost || 0),
      0
    );

  }, [subscriptions]);


  const categories = useMemo(() => {

    const result = {};

    subscriptions.forEach(item => {

      const category = item.category || "Other";

      result[category] =
        (result[category] || 0) +
        Number(item.annual_cost || 0);

    });

    return Object.entries(result).map(
      ([name, value]) => ({
        name,
        value: Math.round(value),
      })
    );

  }, [subscriptions]);


  const frequencyData = useMemo(() => {

    const result = {};

    subscriptions.forEach(item => {

      const frequency =
        item.frequency || "Unknown";

      result[frequency] =
        (result[frequency] || 0) + 1;

    });

    return Object.entries(result).map(
      ([name, value]) => ({
        name,
        subscriptions: value,
      })
    );

  }, [subscriptions]);


  return (
    <div className="dashboard">

      {/* Header */}

      <div className="dashboard-header">

        <div>
          <h1>Subscription Auditor</h1>

          <p>
            Analyze your bank transactions
            and discover recurring payments.
          </p>
        </div>

      </div>


      {/* Summary Cards */}

      <div className="stats-grid">

        <div className="stat-card">

          <span>
            Transactions
          </span>

          <strong>
            {data.transaction_count || 0}
          </strong>

        </div>


        <div className="stat-card">

          <span>
            Subscriptions
          </span>

          <strong>
            {data.subscription_count || 0}
          </strong>

        </div>


        <div className="stat-card">

          <span>
            Monthly Cost
          </span>

          <strong>
            ₹{totalMonthly.toLocaleString(
              "en-IN",
              {
                maximumFractionDigits: 0
              }
            )}
          </strong>

        </div>


        <div className="stat-card">

          <span>
            Annual Cost
          </span>

          <strong>
            ₹{totalAnnual.toLocaleString(
              "en-IN",
              {
                maximumFractionDigits: 0
              }
            )}
          </strong>

        </div>

      </div>


      {/* Charts */}

      <div className="charts-grid">

        {/* Category Chart */}

        <div className="chart-card">

          <h2>
            Annual Spending by Category
          </h2>

          {categories.length > 0 ? (

            <ResponsiveContainer
              width="100%"
              height={300}
            >

              <PieChart>

                <Pie
                  data={categories}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label
                >

                  {categories.map(
                    (entry, index) => (
                      <Cell
                        key={index}
                      />
                    )
                  )}

                </Pie>

                <Tooltip
                  formatter={(value) =>
                    `₹${Number(value).toLocaleString(
                      "en-IN"
                    )}`
                  }
                />

              </PieChart>

            </ResponsiveContainer>

          ) : (

            <p>
              No category data available.
            </p>

          )}

        </div>


        {/* Frequency Chart */}

        <div className="chart-card">

          <h2>
            Subscription Frequency
          </h2>

          {frequencyData.length > 0 ? (

            <ResponsiveContainer
              width="100%"
              height={300}
            >

              <BarChart
                data={frequencyData}
              >

                <CartesianGrid />

                <XAxis
                  dataKey="name"
                />

                <YAxis
                  allowDecimals={false}
                />

                <Tooltip />

                <Bar
                  dataKey="subscriptions"
                />

              </BarChart>

            </ResponsiveContainer>

          ) : (

            <p>
              No frequency data available.
            </p>

          )}

        </div>

      </div>


      {/* Subscription Table */}

      <div className="table-card">

        <div className="table-header">

          <div>

            <h2>
              Detected Subscriptions
            </h2>

            <p>
              Recurring payments identified
              from your statement.
            </p>

          </div>

        </div>


        {subscriptions.length === 0 ? (

          <div className="no-data">

            <h3>
              No subscriptions detected
            </h3>

            <p>
              Try uploading a statement
              containing recurring payments.
            </p>

          </div>

        ) : (

          <div className="table-wrapper">

            <table>

              <thead>

                <tr>

                  <th>Merchant</th>

                  <th>Category</th>

                  <th>Frequency</th>

                  <th>Avg. Amount</th>

                  <th>Monthly</th>

                  <th>Annual</th>

                  <th>Transactions</th>

                  <th>Confidence</th>

                </tr>

              </thead>


              <tbody>

                {subscriptions.map(
                  (item, index) => (

                    <tr key={index}>

                      <td>
                        <strong>
                          {item.merchant}
                        </strong>
                      </td>

                      <td>
                        {item.category}
                      </td>

                      <td>
                        <span className="frequency">
                          {item.frequency}
                        </span>
                      </td>

                      <td>
                        ₹{Number(
                          item.average_amount
                        ).toLocaleString(
                          "en-IN"
                        )}
                      </td>

                      <td>
                        ₹{Number(
                          item.monthly_cost
                        ).toLocaleString(
                          "en-IN",
                          {
                            maximumFractionDigits: 0
                          }
                        )}
                      </td>

                      <td>
                        ₹{Number(
                          item.annual_cost
                        ).toLocaleString(
                          "en-IN",
                          {
                            maximumFractionDigits: 0
                          }
                        )}
                      </td>

                      <td>
                        {item.transaction_count}
                      </td>

                      <td>

                        <div className="confidence">

                          <div
                            className="confidence-bar"
                          >

                            <div
                              className="confidence-fill"
                              style={{
                                width:
                                  `${item.confidence}%`
                              }}
                            />

                          </div>

                          <span>
                            {item.confidence}%
                          </span>

                        </div>

                      </td>

                    </tr>

                  )
                )}

              </tbody>

            </table>

          </div>

        )}

      </div>


      {/* Recent Transactions */}

      <div className="table-card">

        <h2>
          Recent Transactions
        </h2>

        <div className="table-wrapper">

          <table>

            <thead>

              <tr>

                <th>Date</th>
                <th>Merchant</th>
                <th>Description</th>
                <th>Amount</th>

              </tr>

            </thead>

            <tbody>

              {transactions
                .slice()
                .reverse()
                .slice(0, 15)
                .map(
                  (transaction, index) => (

                    <tr key={index}>

                      <td>
                        {transaction.date}
                      </td>

                      <td>
                        {transaction.merchant}
                      </td>

                      <td>
                        {transaction.description}
                      </td>

                      <td>
                        ₹{Number(
                          transaction.amount
                        ).toLocaleString(
                          "en-IN"
                        )}
                      </td>

                    </tr>

                  )
                )}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}

export default Dashboard;