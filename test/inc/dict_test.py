import eons
@eons.kind(eons.Functor)
def dict_test(
	container
):
	print(f"{container.name}: {str(container)}")
	print(f"{container.name} as a list: {str(list(container))}")
	print(f"{container.name} as a dict: {str(dict(container))}")