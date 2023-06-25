import React from "react";
import './modalExpenses.css';

function ModalExpenses({modalExpensesOpen, setModalExpensesOpen}) {

    return(
        <div className={modalExpensesOpen ? "modal__expenses active" : "modal__expenses"}>
            <div className="modal__expenses__content">
                <div className="modal__expenses__content__item">
                    <h2>Аренда:</h2>
                    <h2>10.000 Тг</h2>
                </div>
                <div className="modal__expenses__content__item">
                    <h2>Доп материалы:</h2>
                    <h2>10.000 Тг</h2>
                </div>
                <div className="modal__expenses__content__item">
                    <h2>Общая сумма: </h2>
                    <h2>10.000 Тг</h2>
                </div>
                <div className="modal__expenses__content__item">
                    <h2>С игрока: </h2>
                    <h2>10.000 Тг</h2>
                </div>
                <button onClick={() => setModalExpensesOpen(false)}>Оплатить</button>
            </div>
        </div>
    )

}

export default ModalExpenses;