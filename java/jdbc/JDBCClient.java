import java.sql.*;
import java.util.Date;
import java.util.Properties;

class JDBCClient {

  public static void main(String[] args) throws SQLException {
    Connection conn = null;
    Statement stmt = null;
    ResultSet rs = null;

    try {
      try {
        System.out.println("Loading non-XA drivers ...");
        Class.forName("com.mysql.jdbc.Driver").newInstance();
        System.out.println("Non-XA drivers loaded");
      } catch (ClassNotFoundException e) {
      }

      Properties props = new Properties();
      props.setProperty("user", "sysbench");
      props.setProperty("password", "123456");

      conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/sysbench?useServerPrepStmts=true&useSSL=false&useServerPrepStmts=false", props);

      String query = "SELECT transaction_date from table1 UNION ALL SELECT transaction_date from table1";

      System.out.println("Executing query: " + query);
      long startTime = System.currentTimeMillis();

      System.out.println("Preparing query...");
      stmt = conn.prepareStatement(query);
      rs = ((PreparedStatement)stmt).executeQuery();
      long endTime = System.currentTimeMillis();

      if (rs.next()) {
        System.out.println("Got a result after " + (endTime - startTime) + " ms");
      } else {
        System.out.println("No results after " + (endTime - startTime) + " ms");
      }
      System.out.println("Disconnected from database");
    } catch (SQLException e) {
      e.printStackTrace();
    } catch (Exception e) {
      e.printStackTrace();
    } finally {
      if (conn != null) {
        conn.close();
      }
      if (stmt != null) {
        stmt.close();
      }
      if (rs != null) {
        rs.close();
      }
    }
    System.out.println("Complete.");
  }
}
