import React from "react";
import Form from "react-bootstrap/Form";
import "./SelectionPanel.css"

const SelectionPanel = (props) => {




    return (
        <div className="sidebar">
            <h3 className="text-center mt-2">MAIN MENU</h3>
            <hr className="mt-2 mb-3" />

            <div className="container">
                <div className="row">
                    <div className="col-sm-12">
                        Select administrative level
                    </div>
                </div>
                <div className="row mt-2">
                    <Form>
                        <div key={"admin-level-div"} className="mb-3">
                        <Form.Check
                            inline
                            label="One"
                            name="admin-level"
                            type={'radio'}
                            id={"admin-level-1"}
                        />
                        <Form.Check
                            inline
                            label="Two"
                            name="admin-level"
                            type={'radio'}
                            id={"admin-level-2"}
                        />
                        <Form.Check
                            inline
                            label="Three"
                            name="admin-level"
                            type={'radio'}
                            id={"admin-level-3"}
                        />
                        </div>
                    </Form>
                </div>
            </div>
        </div>
    );
};

export default SelectionPanel;