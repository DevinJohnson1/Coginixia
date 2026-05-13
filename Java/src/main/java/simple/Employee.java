package simple;
import java.util.*;

class Department {
    private int deptId;
    private String deptName;

    public Department(int deptId, String deptName) {
        this.deptId = deptId;
        this.deptName = deptName;
    }

    public int getDeptId() {
        return this.deptId;
    }

    public String getDeptName() {
        return this.deptName;
    }

    public void setDeptId(int deptId) {
        this.deptId = deptId;
    }

    public void setDeptName(String deptName) {
        this.deptName = deptName;
    }

    public String toString() {
        return "Department{deptId=" + this.deptId + ", deptName='" + this.deptName + "'}";
    }
}

class Employee {
    private int id;
    private String name;
    private double salary;
    private String deptName;

    public Employee(int id, String name, double salary, String deptName) {
        this.id = id;
        this.name = name;
        this.salary = salary;
        this.deptName = deptName;
    }

    public int getId() {
        return this.id;
    }

    public String getName() {
        return this.name;
    }

    public double getSalary() {
        return this.salary;
    }

    public String getDeptName() {
        return this.deptName;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setSalary(double salary) {
        this.salary = salary;
    }

    public void setDeptName(String deptName) {
        this.deptName = deptName;
    }

    public String toString() {
        return "Employee{id=" + this.id + ", name='" + this.name + "', salary=" + this.salary + ", deptName='" + this.deptName + "'}";
    }

    public static void modifyEmployee(List<Employee> employeeList, int id, String newName, double newSalary, String newDeptName) {
        for (Employee emp : employeeList) {
            if (emp.getId() == id) {
                emp.setName(newName);
                emp.setSalary(newSalary);
                emp.setDeptName(newDeptName);
                System.out.println("Employee with ID " + id + " has been updated: " + emp);
                return;
            }
        }
        System.out.println("Employee with ID " + id + " not found.");
    }

    public static void deleteEmployee(List<Employee> employeeList, int id) {
        Employee toRemove = null;
        for (Employee emp : employeeList) {
            if (emp.getId() == id) {
                toRemove = emp;
                break;
            }
        }
        if (toRemove != null) {
            employeeList.remove(toRemove);
            System.out.println("Employee with ID " + id + " has been deleted.");
        } else {
            System.out.println("Employee with ID " + id + " not found.");
        }
    }

    public static void printAllEmployees(List<Employee> employeeList) {
        if (employeeList == null || employeeList.isEmpty()) {
            System.out.println("No employees to display.");
            return;
        }
        System.out.println("All Employees:");
        for (Employee emp : employeeList) {
            System.out.println("  " + emp);
        }
    }
}

class EmployeeDepartment {
    public static void modifyDepartment(List<Department> deptList, int deptId, String newDeptName) {
        for (Department dept : deptList) {
            if (dept.getDeptId() == deptId) {
                dept.setDeptName(newDeptName);
                System.out.println("Department with ID " + deptId + " has been updated: " + dept);
                return;
            }
        }
        System.out.println("Department with ID " + deptId + " not found.");
    }

    public static void deleteDepartment(List<Department> deptList, int deptId) {
        Department toRemove = null;
        for (Department dept : deptList) {
            if (dept.getDeptId() == deptId) {
                toRemove = dept;
                break;
            }
        }
        if (toRemove != null) {
            deptList.remove(toRemove);
            System.out.println("Department with ID " + deptId + " has been deleted.");
        } else {
            System.out.println("Department with ID " + deptId + " not found.");
        }
    }

    public static void printAllDepartments(List<Department> deptList) {
        if (deptList == null || deptList.isEmpty()) {
            System.out.println("No departments to display.");
            return;
        }
        System.out.println("All Departments:");
        for (Department dept : deptList) {
            System.out.println("  " + dept);
        }
    }

    public static void main(String[] args) {
        // --- Departments ---
        List<Department> departments = new ArrayList<>();
        departments.add(new Department(1, "Engineering"));
        departments.add(new Department(2, "Marketing"));
        departments.add(new Department(3, "Human Resources"));

        printAllDepartments(departments);
        System.out.println();

        // Modify a department
        modifyDepartment(departments, 2, "Sales & Marketing");
        System.out.println();

        // Delete a department
        deleteDepartment(departments, 3);
        System.out.println();

        printAllDepartments(departments);
        System.out.println();

        // --- Employees ---
        List<Employee> employees = new ArrayList<>();
        employees.add(new Employee(101, "Alice Johnson", 85000.00, "Engineering"));
        employees.add(new Employee(102, "Bob Smith", 62000.00, "Marketing"));
        employees.add(new Employee(103, "Carol White", 71000.00, "Human Resources"));

        Employee.printAllEmployees(employees);
        System.out.println();

        // Modify an employee
        Employee.modifyEmployee(employees, 102, "Bob Smith", 68000.00, "Sales & Marketing");
        System.out.println();

        // Delete an employee
        Employee.deleteEmployee(employees, 103);
        System.out.println();

        Employee.printAllEmployees(employees);
    }
}