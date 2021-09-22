// if end hoad page => run main() function 
window.addEventListener('load', () => main())

const ANSWER = '25'
const ANSWER_2 = 'Java Script'
let select_button = null;


function main() {

    // Select button answer your user
    let button = document.querySelectorAll('#answer button');
    button.forEach(element => {
        element.addEventListener('click', (e) => {
            let value_bool = (e.target.innerText === ANSWER) ? true : false;

            let rusile = '';
            if (value_bool) {
                e.target.classList.add('button_select', 'right');
                rusile = 'Correct';
            } else {
                e.target.classList.add('button_select', 'wrong');
                rusile = 'Incorrect';
            }

            document.querySelector('#rusile_Q1').innerText = rusile;


            if (select_button != null && select_button != e.path[0]) {

                select_button.classList.remove('button_select', 'wrong', 'right');
            }

            select_button = e.path[0];

        });
    });


    // Check Q2 
    document.querySelector('#button_Q2').addEventListener('click', () => {
        let rusile = document.querySelector('#rusile_Q2');
        const input = document.querySelector('#intput_Q2');

        input.classList.remove('input_right', 'input_wrong');

        if (input.value === ANSWER_2) {
            input.classList.add('input_right');
            rusile.innerText = 'Correct';

        } else {
            input.classList.add('input_wrong');
            rusile.innerText = 'Incorrect';
        }
    })


}