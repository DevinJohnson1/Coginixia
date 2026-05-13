package controllers;

//localhost:8000/api/customers : return all customers as json response
public class CustomerController {
    private CustomerService customerService;

    public CustomerController(CustomerService customerService) {
        super();
        this.customerService = customerService;
    }
    //GET
    //endpoint: /customers
    //Full URL: https://localhost:8000/api/customers OR "BaseURL/api+/endpoint"
    List<Customer> getAllCustomers() {
        return customerService.getAllCustomers();
    }
}
