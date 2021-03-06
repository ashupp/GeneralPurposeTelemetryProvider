﻿using System;
using System.Reflection;

namespace SimFeedback.telemetry
{
    public class GeneralPurposeTelemetryInfo : EventArgs, TelemetryInfo
    {
        private TelemetryData _telemetryData;

        public GeneralPurposeTelemetryInfo(TelemetryData telemetryData)
        {
            _telemetryData = telemetryData;
        }

        public TelemetryValue TelemetryValueByName(string name)
        {
            GeneralPurposeTelemetryValue tv;
            switch (name)
            {
                default:
                    object data;
                    Type eleDataType = typeof(TelemetryData);
                    PropertyInfo propertyInfo;
                    FieldInfo fieldInfo = eleDataType.GetField(name);
                    if (fieldInfo != null)
                    {
                        data = fieldInfo.GetValue(_telemetryData);
                    }
                    else if ((propertyInfo = eleDataType.GetProperty(name)) != null)
                    {
                        data = propertyInfo.GetValue(_telemetryData, null);
                    }
                    else
                    {
                        throw new UnknownTelemetryValueException(name);
                    }
                    tv = new GeneralPurposeTelemetryValue(name, data);
                    object value = tv.Value;
                    if (value == null)
                    {
                        throw new UnknownTelemetryValueException(name);
                    }

                    break;
            }

            return tv;
        }
    }
}