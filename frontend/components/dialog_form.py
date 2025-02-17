from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import Qt

class DialogForm(QDialog):
    def __init__(self, title, pedido_id=None):
        super().__init__()

        self.setWindowTitle(title)
        self.setGeometry(150, 150, 400, 200)

        self.pedido_id = pedido_id
        self.layout = QVBoxLayout()

        # Formulário de entrada
        self.form_layout = QFormLayout()
        self.descricao_input = QLineEdit()
        self.form_layout.addRow("Descrição", self.descricao_input)

        self.status_input = QComboBox()
        self.status_input.addItems(["pendente", "concluído", "cancelado"])
        self.form_layout.addRow("Status", self.status_input)

        self.valor_input = QLineEdit()
        self.valor_input.setValidator(QDoubleValidator(0.0, 999999.99, 2))  # Apenas números com 2 casas decimais
        self.form_layout.addRow("Valor Total", self.valor_input)

        self.layout.addLayout(self.form_layout)

        # Botões
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.validate_and_accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

        self.setLayout(self.layout)

    def validate_and_accept(self):
        if not self.descricao_input.text() or not self.valor_input.text():
            return  # Não fecha o diálogo se os campos estiverem vazios
        self.accept()

    def get_data(self):
        return {
            "descricao": self.descricao_input.text(),
            "status": self.status_input.currentText(),
            "valor_total": float(self.valor_input.text())
        }
