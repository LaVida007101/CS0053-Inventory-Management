package lib;

import java.util.List;
import java.util.Map;

public class Product {
    public int id;
    public double price;
    public int stockLevel;
    public String name;
    public int soldQuantity;
    public int reorderLevel;
    public double costPerUnit;
    public List<String> inventoryDates;
    public Map<String, Integer> salesDates;
}
