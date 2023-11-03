package lib;
import java.util.Map;

public class Sales {

    public static void addSalesData(Map<Integer, Product> products) {
        String Option = "ADD SALES DATA";
        System.out.println("\n" + PrintFormat.lines(PrintFormat.SCREEN_WIDTH) + PrintFormat.centerText(Option, PrintFormat.SCREEN_WIDTH) + "\n" + PrintFormat.lines(PrintFormat.SCREEN_WIDTH));

        int id = 0;
        Utility.validateAndAssignInput(id, "Enter product ID:");

        if (products.containsKey(id)) {
            Product product = products.get(id);
            int noProductsSold = 0;
            Utility.validateAndAssignInput(noProductsSold, "Enter number of Products Sold:");

            if (noProductsSold <= product.stockLevel && noProductsSold >= 0) {
                product.stockLevel -= noProductsSold;
                product.soldQuantity += noProductsSold;
                product.salesDates.put(Utility.getCurrentDate(), noProductsSold);
                System.out.println("\n**Sales Data Recorded!");
            } else {
                System.out.println("\n**Sales Data Not Recorded. Invalid Value Entered");
            }
        } else {
            System.out.println("\n**Product not found with ID " + id);
        }
    }

    public static void viewSalesData(Map<Integer, Product> products) {
        String Option = "SALES DATA";
        System.out.println("\n" + PrintFormat.lines(PrintFormat.SCREEN_WIDTH) + PrintFormat.centerText(Option, PrintFormat.SCREEN_WIDTH) + "\n" + PrintFormat.lines(PrintFormat.SCREEN_WIDTH));

        System.out.printf("%-" + (PrintFormat.SCREEN_WIDTH / 5) + "s%-" + (2 * (PrintFormat.SCREEN_WIDTH / 5)) + "s%-" + (PrintFormat.SCREEN_WIDTH / 5) + "s%-" + (PrintFormat.SCREEN_WIDTH / 5) + "s%n", "ID", "NAME", "PRICE", "SOLD QUANTITY");
        System.out.println(PrintFormat.dash(PrintFormat.SCREEN_WIDTH));

        for (Product product : products.values()) {
            System.out.printf("%-" + (PrintFormat.SCREEN_WIDTH / 5) + "d%-" + (2 * (PrintFormat.SCREEN_WIDTH / 5)) + "s%-" + (PrintFormat.SCREEN_WIDTH / 5) + ".2f%-" + (PrintFormat.SCREEN_WIDTH / 5) + "d%n",
                    product.id, product.name, product.price, product.soldQuantity);
        }

        System.out.println("\n" + PrintFormat.lines(PrintFormat.SCREEN_WIDTH));
    }

    public static void generateReports(Map<Integer, Product> products) {
        String Option = "REPORTS";
        System.out.println("\n" + PrintFormat.lines(PrintFormat.SCREEN_WIDTH) + PrintFormat.centerText(Option, PrintFormat.SCREEN_WIDTH) + "\n" + PrintFormat.lines(PrintFormat.SCREEN_WIDTH));
        double totalSales = 0.0;
        double totalCost = 0.0;

        for (Product product : products.values()) {

            double revenue = product.soldQuantity * product.price;
            double cost = product.soldQuantity * product.costPerUnit;
            totalSales += revenue;
            totalCost += cost;

            int soldInTimeFrame = 0;
            for (Map.Entry<String, Integer> date : product.salesDates.entrySet()) {
                soldInTimeFrame += date.getValue();
            }

            int lastDays = 0;
            if (product.salesDates.isEmpty()) {
                lastDays = Utility.dateDifference(product.inventoryDates.get(product.inventoryDates.size() - 1));
            } else {
                lastDays = Utility.dateDifference(product.salesDates.entrySet().iterator().next().getKey());
            }
            System.out.println();
            System.out.printf("%-" + (PrintFormat.SCREEN_WIDTH / 3) + "s%d%n", "ID:", product.id);
            System.out.printf("%-" + (PrintFormat.SCREEN_WIDTH / 3) + "s%s%n", "PRODUCT:", product.name);
            System.out.printf("%-" + (PrintFormat.SCREEN_WIDTH / 3) + "s%d%n", "Sold Quantity:", product.soldQuantity);
            System.out.printf("%-" + (PrintFormat.SCREEN_WIDTH / 3) + "s%s%s%d%s%n", "Sales History:", soldInTimeFrame, " sold within the last ", lastDays, " days.");
            System.out.printf("%-" + (PrintFormat.SCREEN_WIDTH / 3) + "s%s%.2f%n", "Revenue:", "$", revenue);
            System.out.printf("%-" + (PrintFormat.SCREEN_WIDTH / 3) + "s%s%.2f%n", "Total Cost of Goods Sold:", "$", cost);
            System.out.printf("%-" + (PrintFormat.SCREEN_WIDTH / 3) + "s%.2f%s%n", "Profit Margin:", (revenue - cost) / revenue * 100, "%");
        }

        System.out.println(PrintFormat.dash(PrintFormat.SCREEN_WIDTH) + PrintFormat.centerNote("*** TOTAL SALES ***", PrintFormat.SCREEN_WIDTH));
        System.out.printf("%-" + (PrintFormat.SCREEN_WIDTH / 3) + "s%.2f%n", "Total Revenue:", totalSales);
        System.out.printf("%-" + (PrintFormat.SCREEN_WIDTH / 3) + "s%s%.2f%n", "Total Cost of Goods Sold:", "$", totalCost);
        System.out.printf("%-" + (PrintFormat.SCREEN_WIDTH / 3) + "s%.2f%s%n", "Overall Profit Margin:", (totalSales - totalCost) / totalSales * 100, "%");
    }
}
