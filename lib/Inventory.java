package lib;

import java.util.Scanner;

public class Inventory {
    static Scanner input = new Scanner(System.in);

    public static void createProduct() {
        String Option = "ADDING A PRODUCT";
        System.out.println("\n" + PrintFormat.lines(PrintFormat.SCREEN_WIDTH));
        System.out.println(PrintFormat.centerText(Option, PrintFormat.SCREEN_WIDTH));
        System.out.println(PrintFormat.lines(PrintFormat.SCREEN_WIDTH));
        Product product = new Product();

        System.out.print("Enter product name: ");
        product.name = input.nextLine();

        Utility.validateAndAssignInput(product.stockLevel, "Enter initial stock level:");
        Utility.validateAndAssignInput(product.reorderLevel, "Enter reorder level:");
        Utility.validateAndAssignInput(product.costPerUnit, "Enter cost per unit:");
        Utility.validateAndAssignInput(product.price, "Enter Price:");
        product.inventoryDates.add(Utility.getCurrentDate());

        // Product ID determined by incrementing ID value of most recent product by 1
        product.id = Records.products.isEmpty() ? 1 : Records.products.get(Records.products.size()).id + 1;
        product.soldQuantity = 0;
        Records.products.put(product.id, product);

        System.out.println("\n** Product added successfully.");
    }

    public static void updateProduct() {
        String Option = "UPDATING A PRODUCT";
        System.out.println("\n" + PrintFormat.lines(PrintFormat.SCREEN_WIDTH));
        System.out.println(PrintFormat.centerText(Option, PrintFormat.SCREEN_WIDTH));
        System.out.println(PrintFormat.lines(PrintFormat.SCREEN_WIDTH));

        int id = 0;
        Utility.validateAndAssignInput(id, "Enter product ID:");

        if (Records.products.containsKey(id)) {
            Product product = Records.products.get(id);

            System.out.print("New name (or press Enter to keep the same): ");
            String newName = input.nextLine();
            if (!newName.isEmpty()) {
                product.name = newName;
            }

            System.out.println("Enter the following details to update the product (or -1 to keep the same):");
            System.out.print("\tNew stock level:");
            int newStockLevel = input.nextInt();
            if (newStockLevel != -1) {
                product.stockLevel = newStockLevel;
                product.inventoryDates.add(Utility.getCurrentDate());
            }

            System.out.print("\tNew price:");
            double newPrice = input.nextDouble();
            if (newPrice != -1) {
                product.price = newPrice;
            }
            System.out.println("**Product updated successfully.");
        } else {
            System.out.println("**Product not found with ID " + id);
        }
    }

    public static void deleteProduct() {
        String Option = "DELETING A PRODUCT";
        System.out.println("\n" + PrintFormat.lines(PrintFormat.SCREEN_WIDTH));
        System.out.println(PrintFormat.centerText(Option, PrintFormat.SCREEN_WIDTH));
        System.out.println(PrintFormat.lines(PrintFormat.SCREEN_WIDTH));

        int id = 0;
        Utility.validateAndAssignInput(id, "Enter product ID to delete: ");

        if (Records.products.containsKey(id)) {
            Records.products.remove(id);
            System.out.println("**Product deleted successfully!");
        } else {
            System.out.println("**Product not found with ID " + id);
        }
    }

    public static void viewStockLevels() {
        String Option = "STOCK LEVELS";
        System.out.println("\n" + PrintFormat.lines(PrintFormat.SCREEN_WIDTH));
        System.out.println(PrintFormat.centerText(Option, PrintFormat.SCREEN_WIDTH));
        System.out.println(PrintFormat.lines(PrintFormat.SCREEN_WIDTH));

        System.out.format("%-15s%-35s%-15s%-25s%n", "ID", "NAME", "STOCK LEVEL", "REMARKS");
        System.out.println(PrintFormat.dash(PrintFormat.SCREEN_WIDTH));

        for (Product product : Records.products.values()) {
            System.out.format("%-15s%-35s%-15s", product.id, product.name, product.stockLevel);

            if (product.stockLevel <= product.reorderLevel) {
                System.out.println("**Reorder Alert");
            } else {
                System.out.println("Sufficient Stock");
            }
        }
        System.out.println(PrintFormat.lines(PrintFormat.SCREEN_WIDTH));
    }

    public static void generateReorderAlerts() {
        String Option = "REORDER ALERTS";
        System.out.println("\n" + PrintFormat.lines(PrintFormat.SCREEN_WIDTH));
        System.out.println(PrintFormat.centerText(Option, PrintFormat.SCREEN_WIDTH));
        System.out.println(PrintFormat.lines(PrintFormat.SCREEN_WIDTH));

        for (Product product : Records.products.values()) {
            if (product.stockLevel <= product.reorderLevel) {
                System.out.println("Reorder suggested for: ");
                System.out.println("\tProduct ID: \t\t" + product.id);
                System.out.println("\tProduct Name: \t\t" + product.name);
                System.out.println("\tProduct Stock Level: \t" + product.stockLevel);
                System.out.println("\tProduct Reorder Level: \t" + product.reorderLevel + "\n");
            }
        }
    }
}
