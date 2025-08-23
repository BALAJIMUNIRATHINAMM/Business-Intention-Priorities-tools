import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Signal, Upload, Download, AlertCircle } from 'lucide-react';
import { useAnalytics } from '../../contexts/AnalyticsContext';
import { DataProcessor } from '../../lib/dataProcessing';
import { fileUtils } from '../../lib/fileUtils';
import FileUpload from '../../components/FileUpload';
import DataTable from '../../components/DataTable';
import LoadingSpinner from '../../components/LoadingSpinner';
import { ExtractedPriority } from '../../types';
import toast from 'react-hot-toast';

const SignalBF: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [extractedData, setExtractedData] = useState<ExtractedPriority[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const { track } = useAnalytics();

  useEffect(() => {
    track('tool_accessed', { tool: 'Signal BF' });
  }, []);

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setExtractedData([]);
    track('file_uploaded', { tool: 'Signal BF', filename: file.name, size: file.size });
  };

  const handleFileRemove = () => {
    setSelectedFile(null);
    setExtractedData([]);
  };

  const processFile = async () => {
    if (!selectedFile) return;

    setIsProcessing(true);
    try {
      const rawData = await fileUtils.parseFile(selectedFile);
      
      // Validate required columns
      const requiredColumns = ['Company', 'Publication Month', 'Months Considered', 'Highlights Month', 'Priority Type', 'Formatted Priorities'];
      const firstRow = rawData[0] || {};
      const missingColumns = requiredColumns.filter(col => !(col in firstRow));
      
      if (missingColumns.length > 0) {
        throw new Error(`Missing required columns: ${missingColumns.join(', ')}`);
      }

      const processed = await DataProcessor.processSignalBF(rawData);
      setExtractedData(processed);
      
      track('file_processed', { 
        tool: 'Signal BF', 
        filename: selectedFile.name,
        recordsProcessed: processed.length 
      });
      
      toast.success(`Successfully processed ${processed.length} priority records!`);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Processing failed';
      toast.error(message);
      track('processing_error', { tool: 'Signal BF', error: message });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownload = (format: 'csv' | 'excel') => {
    if (extractedData.length === 0) return;
    
    const filename = fileUtils.generateFilename('signal_priorities', format);
    
    if (format === 'csv') {
      fileUtils.downloadCSV(extractedData, filename);
    } else {
      fileUtils.downloadExcel(extractedData, filename);
    }
    
    track('file_downloaded', { tool: 'Signal BF', format, filename });
    toast.success(`Downloaded ${format.toUpperCase()} file successfully!`);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
          <Signal className="h-8 w-8 text-blue-600" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Signal BF Priority Extraction</h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Extract and analyze priority signals from business function data with advanced processing capabilities
        </p>
      </motion.div>

      {/* Instructions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card bg-blue-50 border-blue-200"
      >
        <div className="flex items-start space-x-3">
          <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5" />
          <div>
            <h3 className="font-medium text-blue-900 mb-2">Required File Format</h3>
            <p className="text-sm text-blue-800 mb-3">
              Your file must contain the following columns:
            </p>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2 text-sm text-blue-700">
              <span className="font-mono bg-blue-100 px-2 py-1 rounded">Company</span>
              <span className="font-mono bg-blue-100 px-2 py-1 rounded">Publication Month</span>
              <span className="font-mono bg-blue-100 px-2 py-1 rounded">Months Considered</span>
              <span className="font-mono bg-blue-100 px-2 py-1 rounded">Highlights Month</span>
              <span className="font-mono bg-blue-100 px-2 py-1 rounded">Priority Type</span>
              <span className="font-mono bg-blue-100 px-2 py-1 rounded">Formatted Priorities</span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* File Upload */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <FileUpload
          onFileSelect={handleFileSelect}
          selectedFile={selectedFile || undefined}
          onFileRemove={handleFileRemove}
          disabled={isProcessing}
        />
      </motion.div>

      {/* Process Button */}
      {selectedFile && !isProcessing && extractedData.length === 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="text-center"
        >
          <button
            onClick={processFile}
            className="btn-primary text-lg px-8 py-3"
          >
            <Upload className="h-5 w-5 mr-2" />
            Process Signal Data
          </button>
        </motion.div>
      )}

      {/* Processing State */}
      {isProcessing && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="card text-center py-12"
        >
          <LoadingSpinner size="lg" text="Processing signal data..." />
        </motion.div>
      )}

      {/* Results */}
      {extractedData.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900">
              Extracted Priorities ({extractedData.length} records)
            </h2>
          </div>
          
          <DataTable
            data={extractedData}
            onDownload={handleDownload}
          />
        </motion.div>
      )}
    </div>
  );
};

export default SignalBF;