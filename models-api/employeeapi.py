from flask import Response, jsonify
from database import db
from models.employee import Employee
from schemas import EmployeeSchema

def list_employees():
    """
    if the request method is get and the path is /employees the function home will return the list of employees
    """
    all_employees = get_employees()
    if all_employees is not None:
        return all_employees, 200
    return {"Error": "no employees found"}, 404


def get_employees() -> Response:
    """
    get_items will return all the employee records stored in the database
    Returns:
        Response: a json response of all the employee records
    """
    employee_schema = EmployeeSchema(many=True)
    all_employees = Employee.query.all()
    return jsonify(employee_schema.dump(all_employees))


def add_employee(*args, **kwargs):
    """
    if the request method is POST and the path is /employees the function add_employee will add the employee in the
     request body to the employees table, and it returns its id
    """
    employee_data_dictionary = kwargs.get("body")
    print(employee_data_dictionary)
    exists = check_exist_employee(employee_data_dictionary)
    if exists:
        return {"Error": "The employee you're are trying to add already exists"}, 500

    else:
        employee = Employee(**employee_data_dictionary)
        try:
            db.session.add(employee)
            db.session.commit()
        except Exception:
            return 'There was an issue adding the employee data'
    return {"Employee ID": employee_data_dictionary['id']}, 201


def check_exist_employee(dictionary_of_employee: dict) -> bool:
    """
    The check_exist_employee function reads the employee dictionary and checks if the employee passed in the post body
     exits or not
    Args:
      dictionary_of_employee(dict): the dictionary containing the employee information
    Returns:
         boolean: if the employee exits or not
    """
    employees = Employee.query.all()
    if employees is None:
        return False
    for employee in employees:
        if employee.id == dictionary_of_employee['id']:
            return True


def employee_details(id: int):
    """
    if the request method is get and the path is /employees/employeeID the function return_user will return the employee
    with the id specified in path
    """
    employee = Employee.query.get_or_404(id)
    employee_schema = EmployeeSchema()
    return jsonify(employee_schema.dump(employee))


def update_employee(*args, **kwargs):
    """
    if the request method is PUT and the path is /employees/employeeid the function update_employee will update the
    employee data in the request body
    """
    employee_id_update = kwargs.get("id")
    employee_data_dictionary = kwargs.get("body")
    exists = check_exist_employee(employee_data_dictionary)
    if exists:
        update_employee_data(employee_data_dictionary, employee_id_update)
        updated_employee = employee_details(employee_id_update)
        return updated_employee, 201


def update_employee_data(employee_data: dict, id: int) -> None:
    """
    The update_employee_data function reads the request body data to be updated and updates that employee
    information
    Args:
      employee_data(dict): the dictionary containing the new information of the employee
      id(int): the id of the employee to be updated
    Returns:
        None
    """
    employee = Employee.query.get_or_404(id)
    employee.name = employee_data['name']
    employee.phoneNumber = employee_data['phoneNumber']
    employee.role = employee_data['role']
    employee.work_status = employee_data['work_status']
    db.session.commit()
    
