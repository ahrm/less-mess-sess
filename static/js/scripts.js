function add_class(prev,newclass)
{
	return prev + ' ' + newclass;
}

function pop_class(prev)
{
	classes = prev.split(' ');
	if (classes.length == 1) //we don't want to remove the initial class
	{
		return prev;
	}
	newclass = '';
	for (var i = 0; i < classes.length - 1;i++)
	{
		newclass += classes[i];
	}
	return newclass;
}

function item_onclick(o)
{
	var checkbox = o.getElementsByTagName('input')[0];

	checkbox.checked = !checkbox.checked;
	if (checkbox.checked)
	{
		o.className = add_class(o.className,"sellistelem")
	}
	else
	{
		o.className = pop_class(o.className);
	}
	
	
}