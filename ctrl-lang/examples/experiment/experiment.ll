define i32 @"main"(i32 %"n")
{
	entry:
		%".0" = alloca [5 x i32]
		%".1" = add i32 0, 0
		%".2" = add i32 0, 1
		%".3" = add i32 0, 2
		%".4" = add i32 0, 3
		%".5" = add i32 0, 4
		%".6" = call i32 @"square" (i32 %"n")
		ret i32 %".6"
}


define i32 @"fact"(i32 %"n")
{
	entry:
		%".0" = icmp eq i32 %"n", 0
		br i1 %".0", label %case.0, label %pattern.1
	pattern.1:
		%".1" = icmp eq i32 %"n", %"n"
		br i1 %".1", label %case.1, label %pattern.error
	pattern.error:
		br label %case.0
	case.0:
		%".2" = add i32 0, 1
		br label %end
	case.1:
		%".3" = add i32 0, 1
		%".4" = sub i32 %"n", %".3"
		%".5" = call i32 @"fact" (i32 %".4")
		%".6" = mul i32 %"n", %".5"
		br label %end
	end:
		%".7" = phi i32 [%".2", %case.0], [%".6", %case.1]
		ret i32 %".7"
}


define i32 @"square"(i32 %"n")
{
	entry:
		%".0" = mul i32 %"n", %"n"
		ret i32 %".0"
}


