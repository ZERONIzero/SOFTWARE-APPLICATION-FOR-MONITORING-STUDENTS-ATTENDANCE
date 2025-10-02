document.querySelectorAll('.code').forEach((input, index, inputs) => {
    input.addEventListener('input', function() {
        if (this.value.length >= this.maxLength) {
            const nextInput = inputs[index + 1];
            if (nextInput) {
                nextInput.focus();
            }
        }
    });
});