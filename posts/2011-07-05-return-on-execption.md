---
title: ReturnOnException Aspect (postsharp)
author: Adam Bell
tags: c#, postsharp, aop
---
```
public static class ExceptionHandler
{

 [Serializable]  
 public class ReturnOnException : OnExceptionAspect  
 {  
   public ReturnOnException(object objectToReturn)  
   {  
     _objectToReturn = objectToReturn;  
   }  

   object _objectToReturn;  

   public override void OnException(MethodExecutionEventArgs eventArgs)  
   {  
     string message = eventArgs.Exception.Message;  
     eventArgs.FlowBehavior = FlowBehavior.Return;  
     eventArgs.ReturnValue = _objectToReturn;  
   }  
 }

}
```
Usage:

```
//returns -1 on any error

[ExceptionHandler.ReturnOnException(-1)]

public int DivideBy(int number, int dividedby)  
{  
  return number / dividedby;  
}
```
