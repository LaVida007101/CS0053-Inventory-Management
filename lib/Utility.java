package lib;
import java.io.*;
import java.util.*;
import java.text.ParseException;
import java.text.SimpleDateFormat;

public class Utility {
    // Ensures proper input type is entered by the user
    public static void validateAndAssignInput(Object productProperty, String prompt) {
        boolean inputValid = false;
        Scanner scanner = new Scanner(System.in);

        do {
            String input = scanner.nextLine();
            System.out.print(prompt);

            try{
                if(productProperty instanceof Integer)
                    productProperty = Integer.parseInt(input);
                else if(productProperty instanceof Double)
                    productProperty = Double.parseDouble(input);
                else
                    productProperty = input;
            }
            catch(NumberFormatException e){
            }
        } while (!inputValid);

        scanner.close();
    }

    public static String getCurrentDate() {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date currentDate = new Date();
        return dateFormat.format(currentDate);
    }

    public static int dateDifference(String dateRecordString) {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        try {
            Date inputDate = dateFormat.parse(dateRecordString);
            Date currentDate = new Date();
            long difference = currentDate.getTime() - inputDate.getTime();
            int daysDifference = (int) (difference / (1000 * 60 * 60 * 24));
            return daysDifference;
        } catch (ParseException e) {
            // Handle the parsing exception here
            e.printStackTrace();
            return 0;
        }
    }

    public static void clearTerminal() {
        System.out.print("\033[H\033[2J");
        System.out.flush();
    }

    public static void displayMainMenu() {
    }

    public static void saveDataToFile(String dataFileName, String inventoryStockingFileName, String salesData) {
         try {
            PrintWriter dataFile = new PrintWriter(dataFileName);
            PrintWriter stockingFile = new PrintWriter(inventoryStockingFileName);
            PrintWriter salesFile = new PrintWriter(salesData);

            for (Map.Entry<Integer, Product> entry : Records.products.entrySet()) {
                Product product = entry.getValue();
                dataFile.println(product.id + "," + product.name + "," + product.stockLevel + ","
                        + String.format("%.2f", product.costPerUnit) + "," + product.price + ","
                        + product.soldQuantity + "," + product.reorderLevel);

                for (String stockDate : product.inventoryDates) {
                    stockingFile.println(product.id + "," + stockDate);
                }

                for (Map.Entry<String, Integer> salesEntry : product.salesDates.entrySet()) {
                    salesFile.println(product.id + "," + salesEntry.getKey() + "," + salesEntry.getValue());
                }
            }

            dataFile.close();
            stockingFile.close();
            salesFile.close();
            System.out.println("\n" + PrintFormat.dash(PrintFormat.SCREEN_WIDTH) + "\n**Data saved to " + dataFileName);
        } catch (IOException e) {
            // Handle the file IO exception here
            e.printStackTrace();
            System.err.println("\n" + PrintFormat.dash(PrintFormat.SCREEN_WIDTH) + "\n**Error: Unable to open the data file for saving.");
        }
    }

    public static void loadDataFromFile(String dataFileName, String inventoryStockingFileName, String salesData) {
        Records.products.clear(); // Clear existing data

        try {
            BufferedReader dataFile = new BufferedReader(new FileReader(dataFileName));
            BufferedReader stockingFile = new BufferedReader(new FileReader(inventoryStockingFileName));
            BufferedReader salesFile = new BufferedReader(new FileReader(salesData));

            String line;

            while ((line = dataFile.readLine()) != null) {
                String[] fields = line.split(",");
                Product product = new Product();
                product.id = Integer.parseInt(fields[0]);
                product.name = fields[1];
                product.stockLevel = Integer.parseInt(fields[2]);
                product.costPerUnit = Double.parseDouble(fields[3]);
                product.price = Integer.parseInt(fields[4]);
                product.soldQuantity = Integer.parseInt(fields[5]);
                product.reorderLevel = Integer.parseInt(fields[6]);

                while ((line = stockingFile.readLine()) != null) {
                    String[] stockingFields = line.split(",");
                    if (product.id == Integer.parseInt(stockingFields[0])) {
                        product.inventoryDates.add(stockingFields[1]);
                    }
                }
                stockingFile.close();

                while ((line = salesFile.readLine()) != null) {
                    String[] salesFields = line.split(",");
                    if (product.id == Integer.parseInt(salesFields[0])) {
                        product.salesDates.put(salesFields[1], Integer.parseInt(salesFields[2]));
                    }
                }
                salesFile.close();

                if (!product.salesDates.isEmpty()) {
                    String firstSalesDate = product.salesDates.entrySet().iterator().next().getKey();
                    int daysDifference = dateDifference(firstSalesDate);
                    if (daysDifference >= 90) {
                        product.salesDates.clear();
                    }
                }

                Records.products.put(product.id, product);
            }

            dataFile.close();
            System.out.println("\n" + PrintFormat.dash(PrintFormat.SCREEN_WIDTH) + "\n**Data loaded from " + dataFileName);
        } catch (IOException e) {
            // Handle the file IO exception here
            e.printStackTrace();
            System.out.println("\n" + PrintFormat.dash(PrintFormat.SCREEN_WIDTH) + "\n**No existing data found. Starting with an empty inventory.");
        }
    }
}

