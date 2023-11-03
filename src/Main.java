package src;
import lib.PrintFormat;
import lib.Product;
import lib.Sales;
import lib.Utility;
import lib.Inventory;
import java.util.*;

public class Main {
    public static final String dataFileName = "inventory_data.csv";
    public static final String inventoryStockingFileName = "inventoryStockingRecords.csv";
    public static final String salesData = "salesdata.csv";
    public static boolean changesSaved = true;
    public static int choice;
    public static Map<Integer, Product> products = new HashMap<>();

    public static void displayMainMenu() {
        String MainMenu = "MAIN MENU";

        System.out.println();
        System.out.println(PrintFormat.lines(PrintFormat.SCREEN_WIDTH));
        System.out.println(PrintFormat.centerText(MainMenu, PrintFormat.SCREEN_WIDTH));
        System.out.println(PrintFormat.lines(PrintFormat.SCREEN_WIDTH));

        boolean reorderAlertExists = false;
        for (Map.Entry<Integer, Product> entry : products.entrySet()) {
            if (entry.getValue().stockLevel <= entry.getValue().reorderLevel) {
                reorderAlertExists = true;
                break;
            }
        }

        if (reorderAlertExists) {
            System.out.println(PrintFormat.centerNote("*** Reorder Alert: Some products are at or below the reorder level. ***", PrintFormat.SCREEN_WIDTH));
            System.out.println("\n");
        }

        System.out.println("1. View Stock Levels");
        System.out.println("2. View Sales Data");
        System.out.println("3. Generate Reorder Alerts");
        System.out.println("4. Generate Reports");
        System.out.println("5. Save Data");
        System.out.println("6. Load Data");
        System.out.println("7. Add Product");
        System.out.println("8. Update Product");
        System.out.println("9. Delete Product");
        System.out.println("10. Add Sales");
        System.out.println("11. Exit");
        System.out.println(PrintFormat.lines(PrintFormat.SCREEN_WIDTH));
        System.out.print("Enter your choice:");
    }

    public static void main(String[] args) {
        Utility.loadDataFromFile(dataFileName, inventoryStockingFileName, salesData);

        Scanner input = new Scanner(System.in);

        do {
            Utility.clearTerminal();
            displayMainMenu();

            choice = input.nextInt();
            Utility.clearTerminal();

            switch (choice) {
                case 1:
                    Inventory.viewStockLevels();
                    break;
                case 2:
                    Sales.viewSalesData(products);
                    break;
                case 3:
                    Inventory.generateReorderAlerts();
                    break;
                case 4:
                    Sales.generateReports(products);
                    break;
                case 5:
                    Utility.saveDataToFile(dataFileName, inventoryStockingFileName, salesData);
                    changesSaved = true;
                    break;
                case 6:
                    Utility.loadDataFromFile(dataFileName, inventoryStockingFileName, salesData);
                    break;
                case 7:
                    Inventory.createProduct();
                    break;
                case 8:
                    Inventory.updateProduct();
                    break;
                case 9:
                    Inventory.deleteProduct();
                    break;
                case 10:
                    Sales.addSalesData(products);
                    break;
                case 11:
                    if (!changesSaved) {
                        System.out.print("Exit without saving changes? (y/any key): ");
                        char exitProgram = input.next().charAt(0);
                        if (Character.toLowerCase(exitProgram) == 'y') {
                            changesSaved = true;
                        }
                    } else {
                        System.out.println();
                        System.out.println(PrintFormat.lines(PrintFormat.SCREEN_WIDTH));
                        System.out.println("Exiting the Inventory Management System.");
                    }
                    break;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
            

            if (choice >= 7 && choice <= 10) {
                changesSaved = false;
            }

            input.nextLine(); // consumes the newline character
            System.out.print("Press Enter to continue...");
            input.nextLine();
        } while (choice != 11 || !changesSaved);

        input.close();
    }
}
