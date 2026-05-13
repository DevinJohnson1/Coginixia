package services;

import java.util.*;
import models.Customer;
import repo.CustomerRepo;

public class CustomerService {
    private CustomerRepo customerRepo;

    public CustomerService(CustomerRepo customerRepo) {
        super();
        this.customerRepo = customerRepo;
    }

    public List<Customer> getAllCustomers() {
        return customerRepo.getAllCustomers();
    }
}
