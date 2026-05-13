package repo;
import java.util.*;
import models.Customer;

public class CustomerRepo {
    static List<Customer> customers = new ArrayList<>();

    static List<Account> accountsForCustomer2 = new ArrayList<>();
    static List<Account> accountsForCustomer3 = new ArrayList<>();

    static {

        Account acc1 = new Account (1, "Savings", 1000);
        Account acc2 = new Account (2, "Savings", 2000);
        Account acc3 = new Account (3, "Checkings", 2000);


        customer.add(new Customer(1, "Steve Boyo", new ArrayList<>()));
        customer.add(new Customer(2, "Mark Job", accountsForCustomer2));
        customer.add(new Customer(3, "Nolan Job", accountsForCustomer3));
    }

}
