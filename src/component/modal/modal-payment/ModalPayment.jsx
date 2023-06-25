import React from "react";
import './modalPayment.css';

function ModalPayment({modalPaymentOpen, setModalPaymentOpen}) {

    return(
        <div className={modalPaymentOpen ? "modal__payment active" : "modal__payment"}>
            <div className="modal__payment__content">
                <h3>добавьте платёжную систему</h3>
                <h4>Обновите свои платёжные методы</h4>
                <div style={{marginTop: '20px', display: 'flex', justifyContent: 'space-between'}}>
                    <div >
                        <h5>Имя на карте</h5>
                        <input className="input__one" type="text" name="" id="" />
                    </div>
                    <div >
                        <h5>Срок</h5>
                        <input className="input__two" type="text" name="" id="" />
                    </div>
                </div>
                <div style={{marginTop: '15px', display: 'flex', justifyContent: 'space-between'}}>
                    <div >
                        <h5>Номер карты</h5>
                        <input className="input__one" type="text" name="" id="" />
                    </div>
                    <div >
                        <h5>CVV</h5>
                        <input className="input__two" type="password" name="" id="" />
                    </div>
                </div>
                <div  style={{marginTop: '32px', display: 'flex', justifyContent: 'space-between'}}>
                    <button onClick={() => setModalPaymentOpen(false)} className="modal__payment__content__close">Отклонить</button>
                    <button className="modal__payment__content__confirm">Подтвердить</button>
                </div>
            </div>
        </div>
    )

}
export default ModalPayment;