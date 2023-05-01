import pytest
from app.add import add

@pytest.mark.parametrize("num1,num2,expected",[
    (1,2,3),
    (2,5,7),
    (100,0,100),
    (2,9,7)
])
def test_add(num1,num2,expected):
    print("testing add")
    assert add(num1,num2)==expected